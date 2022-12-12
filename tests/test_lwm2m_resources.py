# ----------------------------------------------------------------------------
# Copyright (c) 2022, Izuma Networks
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
# This test file tests use Izuma connect API:
# https://developer.izumanetworks.com/docs/device-management-api/connect/
# to read and write resource values from/to device.
# ----------------------------------------------------------------------------

import logging
import pytest
import random
import base64

from izuma_systest_lib.cloud import connect_handler

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

    resource = '/1/0/1'
    payload = {'method': 'PUT', 'uri': resource, 'payload-b64': lifetime['payload-b64']}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)
    # Test response received with 200 OK status
    assert resp and resp['status'] == 200, 'Unable to update device resource: {} value'.format(resource)


def test_get_lifetime(edge, cloud_api, websocket, lifetime):
    log.info('Get Edge lifetime value. {}'.format(edge.device_id))

    resource = '/1/0/1'
    payload = {'method': 'GET', 'uri': resource}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)

    # Test response received with 200 OK status
    assert resp and resp['status'] == 200, 'Unable to read device resource: {} value'.format(resource)
    # Test payload is expected and decoded correctly
    assert resp.get('decoded_payload') == lifetime['payload'], 'Resource {}value is not expected or ' \
                                                               'decoding error.'.format(resource)
    assert resp.get('payload') == lifetime['payload-b64'], 'Resource {} value is not expected.'.format(resource)
