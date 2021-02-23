import logging
import pytest
import random
import base64

from pelion_systest_lib.cloud import connect_handler

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@pytest.fixture(scope='module')
def lifetime():
    payload = str(random.randint(1000, 3599))
    ascii_value = payload.encode('ascii')
    b64_value = str(base64.b64encode(ascii_value), 'utf-8')

    yield {'payload': payload, 'payload-b64': b64_value}


def test_put_lifetime(edge, cloud_api, websocket, lifetime):
    log.info('Update device: {}, lifetime resource: {} to seconds.'.format(edge.device_id, lifetime))

    payload = {'method': 'PUT', 'uri': '/1/0/1', 'payload-b64': lifetime['payload-b64']}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)
    # Test response received with 200 OK status
    assert resp and resp['status'] == 200, 'Unable to update device resource value'


def test_get_lifetime(edge, cloud_api, websocket, lifetime):
    log.info('Get Edge lifetime value. {}'.format(edge.device_id))

    payload = {'method': 'GET', 'uri': '/1/0/1'}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)

    # Test response received with 200 OK status
    assert resp and resp['status'] == 200, 'Unable to read device resource value'
    # Test payload is expected and decoded correctly
    assert resp.get('decoded_payload') == lifetime['payload']
    assert resp.get('payload') == lifetime['payload-b64']



