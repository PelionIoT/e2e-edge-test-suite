# ----------------------------------------------------------------------------
# Copyright (c) 2020-2021, Pelion and affiliates.
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

# ----------------------------------------------------------------------------
# This test file tests use The Kubernetes command-line tool, kubectl,
# to run commands against Kubernetes clusters.
#
# Tests will check that node can be found from K8S and simple pod creation
# is successful.
#
# Edge k8s must be enabled in your Pelion account to run these test
# successfully.
# ----------------------------------------------------------------------------

import logging
import time
import uuid
import pytest
import os

from pelion_systest_lib.edge.kaas import Kaas
from pelion_systest_lib.edge.kubectl import Kubectl
from pelion_systest_lib.tools import execute_with_retry

log = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def pod(edge, kubectl):
    pod_name = 'test-pod-{}-{}'.format(edge.device_id, str(uuid.uuid1())[:8])
    pod_yaml_file = load_test_pod_content(pod_name, edge.device_id)
    kubectl.create_pod(pod_yaml_file)
    time.sleep(5)

    yield pod_name

    kubectl.delete_pod(pod_name)
    # remove temporary file
    if os.path.exists(pod_yaml_file):
        os.remove(pod_yaml_file)


def test_node(edge):
    response = execute_with_retry(
        command='kubectl get nodes',
        assert_text=edge.device_id)

    assert edge.device_id in response, 'Device not found from K8S'


def test_pod(pod):
    response = execute_with_retry(
        command='kubectl get pods {}'.format(pod),
        assert_text=pod)

    assert 'Error' not in response, 'Pod not found or error message received from server when starting pod'


def test_pod_state(pod):
    for i in range(60):
        response = Kubectl.get_pod_details(pod)
        if response['STATUS'] == 'Running':
            break
        time.sleep(2)

    assert response['STATUS'] == 'Running', 'Pod not in running state'


def load_test_pod_content(pod_name, device_id):
    pod_yaml_file = 'temporary_k8s_kubectl.yaml'
    with open(pod_yaml_file, 'w') as file:
        content = Kaas.get_yaml_template(
            data_folder='data',
            file_name='test_k8s_kubectl.yaml').render(
            pod_name=pod_name,
            node_name=device_id
        )
        log.debug("{} content: {}".format(pod_yaml_file, content))
        file.write(content)
    return pod_yaml_file
