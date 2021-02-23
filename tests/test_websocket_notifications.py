import logging
from pelion_systest_lib.cloud import connect_handler

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def test_registration_update_notification(edge, cloud_api, websocket):
    wait_time = 60

    log.info('Trigger registration update')
    payload = {'method': 'POST', 'uri': '/1/0/8'}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)

    assert resp and resp['status'] == 200, 'Execute (POST) to update resource value is failed'

    log.info('Wait registration update for max {} second(s)'.format(wait_time))
    # check registration update from websocket notification channel
    data = websocket.wait_for_registration_updates(edge.device_id, wait_time)

    assert data, 'Registration update received from websocket notification channel'


def test_registration_notification(edge, cloud_api, websocket):
    wait_time = 3 * 60

    log.info('Rebooting device..')
    payload = {'method': 'POST', 'uri': '/3/0/4'}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)

    assert resp and resp['status'] == 200, 'Execute (POST) to update resource value is failed'

    log.info('Wait registration notification for max {} second(s)..'.format(wait_time))
    # check registration from websocket notification channel
    data = websocket.wait_for_registration(edge.device_id, wait_time)

    assert data, 'Registration not received from websocket notification channel'
