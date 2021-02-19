# pylint: disable=redefined-outer-name
"""
Edge related pytest fixtures
"""

import logging
import os

import pytest
from kubernetes.client import Configuration
from kubernetes.config import load_kube_config

import pelion_systest_lib.tools as utils
from pelion_systest_lib.edge.connection.connector import EdgeConnector
from pelion_systest_lib.edge.kaas import Kaas
from pelion_systest_lib.edge.kubectl import Kubectl

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
