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

import pytest
import logging
import base64
from pelion_systest_lib.cloud import connect_handler
import time

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

    assert data, 'Registration update not received from websocket notification channel'


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


def test_notification_device_cpu_usage(edge, cloud_api, websocket, subscribe_to_resource):
    cpu_usage = '/3/0/3320'
    payload = {'method': 'GET', 'uri': cpu_usage}

    # Check device really have that resource before subscribing it.
    response = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                       channel_type=websocket,
                                                                       ep_id=edge.device_id,
                                                                       apikey=websocket.api_key,
                                                                       payload=payload, async_id=None,
                                                                       timeout=60)
    if response['status'] == 404:
        pytest.skip('Device does not have specific resource: {}.'.format(cpu_usage))

    subscribe_to_resource(cpu_usage)
    time.sleep(10)

    payload = None
    data = websocket.wait_for_resource_notifications(edge.device_id, cpu_usage, timeout=10 * 60, delay=5)

    if data:
        payload = str(base64.b64decode(data['payload']))
        log.info('Current cpu usage: {} %'.format(payload))

    assert payload, 'Unable to get notifications from websocket channel'
