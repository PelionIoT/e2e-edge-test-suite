import base64
import logging
import random
import pytest

from pelion_systest_lib.cloud import connect_handler

log = logging.getLogger(__name__)


class Resources:
    def __init__(self):
        self.lifetime = None


class TestEdgeAttributes:
    """
    Smoke test set for edge-core for cloud and/or edge-core release monitoring.
    - Edge attribute tests
    - Registration update check
    - GET, PUT, POST check
    """
    resource = Resources()

    def test(self, tc_config_data):
        log.info('test')
        log.info(tc_config_data)

    @pytest.mark.edge_smoke
    def test_03_put_edge_lifetime(self, edge, cloud_api, websocket):
        lifetime = random.randint(1000, 3599)
        lifetime_ascii = str(lifetime).encode('ascii')
        lifetime_b64 = str(base64.b64encode(lifetime_ascii), 'utf-8')
        log.info('Set Edge: {}, lifetime: {} seconds.'.format(edge.device_id, lifetime))

        payload = {'method': 'PUT', 'uri': '/1/0/1', 'payload-b64': lifetime_b64}
        resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                       channel_type=websocket,
                                                                       ep_id=edge.device_id,
                                                                       apikey=websocket.api_key,
                                                                       payload=payload, async_id=None)

        assert resp and resp['status'] == 200, 'Put to update resource value is failed'
        self.resource.lifetime = lifetime

    @pytest.mark.edge_smoke
    def test_04_get_edge_lifetime(self, edge, cloud_api, websocket):
        log.info('Get Edge: {} lifetime value. '.format(edge.device_id))

        payload = {'method': 'GET', 'uri': '/1/0/1'}
        resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                       channel_type=websocket,
                                                                       ep_id=edge.device_id,
                                                                       apikey=websocket.api_key,
                                                                       payload=payload, async_id=None)

        assert resp and resp['status'] == 200, 'Get to lifetime resource value is failed. {}'.format(payload)
        lifetime = resp.get('decoded_payload')
        log.info('Lifetime: {}'.format(lifetime))
        assert int(lifetime) == self.resource.lifetime, 'Lifetime value is not expected'

    @pytest.mark.edge_smoke
    def test_05_post_trigger_registration_update(self, edge, cloud_api, websocket):
        wait_time = 60

        log.info('Trigger registration update')
        log.info('Wait registration update for max {} second(s)'.format(wait_time))

        payload = {'method': 'POST', 'uri': '/1/0/8'}
        resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                       channel_type=websocket,
                                                                       ep_id=edge.device_id,
                                                                       apikey=websocket.api_key,
                                                                       payload=payload, async_id=None)

        assert resp and resp['status'] == 200, 'Post to update resource value is failed'

        ts = time.time()
        # check registration update for endpoints
        data = websocket.wait_for_registration_updates(edge.device_id, wait_time)
        te = time.time()

        if not data:
            raise AssertionError(
                'Registration update failed. Triggering reg-update failed or reg-update not received  \
                for edge during {} second(s).'.format(wait_time))

        log.info('Time for registration updates {:.4f} s'.format(te - ts))


import logging
import time

import pytest

from pelion_systest_lib.edge.kaas import Kaas
from pelion_systest_lib.tools import execute_local_command, execute_with_retry

log = logging.getLogger(__name__)


class TestEdgeKaasKubectl:
    """
    Set for testing Snap service locally.
    Test cases are not atomic. Class is defined to run as such.
    """

    @staticmethod
    def load_test_pod_content(pod_name, device_id):
        pod_yaml_file = 'test_pod.yaml'
        with open(pod_yaml_file, 'w') as file:
            content = Kaas.get_yaml_template(
                data_folder='data',
                file_name='test_edge_smoke.yaml').render(
                pod_name=pod_name,
                node_name=device_id
            )
            log.debug("{} content: {}".format(pod_yaml_file, content))
            file.write(content)
        return pod_yaml_file

    @pytest.fixture(scope="class")
    def pod(self, edge, tc_config_data, kubectl):
        # create new pod and delete after test
        pod_name = 'test-pod-syte-{}'.format(edge.device_id)
        pod_yaml_file = self.load_test_pod_content(pod_name, edge.device_id)
        kubectl.create_pod(pod_yaml_file)
        time.sleep(1)  # Wait a bit because idea is not to stress kaas too much

        yield pod_name

        execute_local_command('kubectl delete pods {}  --force --grace-period=0'.format(pod_name))

    def test_01_get_config(self, kubectl, edge):
        """ Checks that configuration looks right, it is important to keep edge fixture here to make sure that
        configuration is done """
        assert edge.tc_config_data.get(
            'edge_k8s_url') in kubectl.view_config(), 'kubectl environment configuration error'

    def test_01_get_clusters(self, kubectl):
        assert 'edge-k8s' in kubectl.get_clusters(), 'kubectl environment configuration error'

    def test_01_get_contexts(self, edge, kubectl):
        assert 'edge-k8s' in kubectl.get_contexts(), 'kubectl environment configuration error'

    def test_02_curl_get_node(self, edge):
        command = "curl -X GET -v   {edge_k8s_url}/api/v1/nodes/{device_id}  -H 'Authorization: Bearer {api_key}'".format(
            edge_k8s_url=edge.tc_config_data.get('edge_k8s_url'),
            device_id=edge.device_id,
            api_key=edge.tc_config_data.get('api_key'))
        # It takes some time that edge is registered in the KaaS
        response = execute_with_retry(command, edge.device_id)
        assert 'NotFound' not in response

    def test_02_kubectl_get_nodes(self, edge):
        response = execute_with_retry(
            command='kubectl get nodes',
            assert_text=edge.device_id)
        assert edge.device_id in response, 'Internal id not found from KAAS nodes list'
