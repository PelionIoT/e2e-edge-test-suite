# ----------------------------------------------------------------------------
# Copyright (c) 2020-2021, Pelion and affiliates.
# Copyright (c) 2022, Izuma Networks
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

# pylint: disable=redefined-outer-name
"""
Edge related pytest fixtures
"""

import logging
import os

import pytest
from kubernetes.client import Configuration
from kubernetes.config import load_kube_config

import izuma_systest_lib.tools as utils
from izuma_systest_lib.edge.connection.connector import EdgeConnector
from izuma_systest_lib.edge.kaas import Kaas
from izuma_systest_lib.edge.kubectl import Kubectl

log = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def kube_config_file_path(tc_config_data):
    """
    Create temporary configuration file
    :param tc_config_data:
    :return:
    """
    kube_config_path = tc_config_data.get('kubernetes_configuration_file', '')
    is_temporary = False

    # If kube configuration file is missing, add it to the disk
    if 'edge_k8s_url' in tc_config_data \
            and 'api_key' in tc_config_data \
            and not kube_config_path:
        log.debug('Creating kubernetes configuration file')
        kube_config_path = Kubectl().write_kubectl_config(
            server_url=tc_config_data['edge_k8s_url'],
            api_key=tc_config_data['api_key'])
        if not os.environ.get('JENKINS_URL', False):
            is_temporary = True

        # Set kubectl to use new configuration file
        os.environ['KUBECONFIG'] = kube_config_path
        log.debug('KUBECONFIG={}'.format(os.environ['KUBECONFIG']))

        # Take configuration in use
        utils.execute_local_command('kubectl config use-context edge-k8s')
        log.debug('Temporary kubernetes configuration successfully created and in use')
    else:
        log.debug('No need to create temporary kubernetes konfiguration')
    yield kube_config_path

    # Remove temporary configuration when running outside Jenkins
    if is_temporary:
        log.debug('Removing temporary kube config: {}'.format(kube_config_path))
        os.remove(kube_config_path)


@pytest.fixture(scope='session')
def edge(kube_config_file_path, tc_config_data):
    """
    Initializes connection to edge via RaaS or locally (subprocess) based on configuration.
    Release connection when not needed anymore
    :param kube_config_file_path: Kubernetes konfiguration file path
    :param tc_config_data: Test case config
    :return: resource
    """
    edge = EdgeConnector(tc_config_data)
    try:
        edge.connect_edge()
    except BaseException as e:
        if not tc_config_data.get('edge_skip_release_if_setup_error', False):
            edge.release()
        raise e

    yield edge

    edge.release()


@pytest.fixture(scope='session')
def kubectl(edge):  # pylint: disable=unused-argument
    return Kubectl()


@pytest.fixture(scope='class')
def kaas(kube_config_file_path):
    """
    Open connection to the kubernets as a service (KAAS) using kubernets python sdk
    :param kube_config_file_path: Kubernetes konfiguration file path
    :return: api_client
    """
    custom_configuration = Configuration()
    custom_configuration.assert_hostname = False
    load_kube_config(client_configuration=custom_configuration, config_file=kube_config_file_path)
    Configuration.set_default(custom_configuration)

    return Kaas(kube_config_file_path)


@pytest.fixture(scope="class")
def kaas_enabled(cloud_api, kubectl):
    response = cloud_api.rest_api_edge_k8s.get('/api/v1/namespaces/default/pods')
    if response.status_code != 200:
        log.error('Failed to connect KaaS. {}'.format(response.text))
        pytest.skip('Make sure Kubernetes For The Edge (edge_k8s) is enabled in your Izuma device management account')

    if not kubectl.kubectl_installed(False):
        pytest.skip('Kubectl not installed. Please check installation notes.')
