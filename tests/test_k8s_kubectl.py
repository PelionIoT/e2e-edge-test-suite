import logging
import time
import uuid
import pytest

from pelion_systest_lib.edge.kaas import Kaas
from pelion_systest_lib.tools import execute_with_retry

log = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def pod(edge, kubectl):
    pod_name = 'test-pod-{}'.format(edge.device_id)
    pod_yaml_file = load_test_pod_content(pod_name, edge.device_id)
    kubectl.create_pod(pod_yaml_file)
    time.sleep(5)

    yield pod_name

    kubectl.delete_pod(pod_name)


def test_node(edge):
    response = execute_with_retry(
        command='kubectl get nodes',
        assert_text=edge.device_id)

    assert edge.device_id in response, 'Device not found from K8S nodes'


def test_pod(pod):
    response = execute_with_retry(
        command='kubectl get pods',
        assert_text=pod)

    log.info(response)


def load_test_pod_content(pod_name, device_id):
    pod_yaml_file = 'test_k8s_kubectl.yaml'
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
