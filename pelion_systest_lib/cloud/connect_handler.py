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

"""
Connect handler related helper functions
"""

import base64
import logging
from time import sleep

import pelion_systest_lib.tools as utils

log = logging.getLogger(__name__)


def send_async_device_and_wait_for_response(cloud_api, channel_type, ep_id, apikey, payload, async_id=None,
                                            timeout=30, expiry_seconds=None):
    """
    Send a get rest request to specific resource and wait for the async response from device
    :param payload: The request we want to send to device for example: {"method": "GET", "uri": "/1000/0/1"}
    :param expiry_seconds: The time period during which the delivery is attempted, in seconds.
    :param async_id: Use provided async id with request or generate a random one for the request
    :param cloud_api:
    :param channel_type: websocket or callback
    :param ep_id: device id
    :param apikey: api key fixture.
    :param timeout: timeout for the async wait
    :return: dict / False (if received from cloud)
    """

    if async_id is None:
        async_id = utils.build_random_string(30)
    cloud_api.connect.send_async_request_to_device(ep_id, payload, async_id=async_id, expiry_seconds=expiry_seconds,
                                                   expected_status_code=202,
                                                   api_key=apikey)
    async_response = channel_type.wait_for_async_response(async_response_id=async_id,
                                                          timeout=timeout,
                                                          assert_errors=True)

    log.info('get async response {}'.format(async_response))
    # check if we get async response and it contains payload
    if async_response and 'payload' in async_response:
        # decode original payload and append in received async response
        async_response['decoded_payload'] = base64.b64decode(async_response['payload']).decode('utf-8')
        return async_response
    return False


def send_get_and_wait_for_response(cloud_api, channel_type, ep_id, apikey, resource_path, timeout=30):
    """
    Send a get rest request to specific resource and wait for the async response from device
    :param cloud_api:
    :param channel_type: websocket or callback
    :param ep_id: device id
    :param apikey:
    :param resource_path: path of the resource to device
    :param timeout: timeout for the async wait
    :return: dict / False (if received from wait_for_async_response)
    """
    # send a get resource request to device
    response = cloud_api.connect.get_device_resources(device_id=ep_id, resource_path=resource_path,
                                                      expected_status_code=202,
                                                      api_key=apikey)
    async_id = response.json()['async-response-id']
    # wait for async response
    async_response = channel_type.wait_for_async_response(async_response_id=async_id, timeout=timeout,
                                                          assert_errors=True)
    log.info('get async response {}'.format(async_response))
    # check if we get async response and it contains payload
    if async_response and 'payload' in async_response:
        # decode original payload and append in received async response
        async_response['decoded_payload'] = base64.b64decode(async_response['payload']).decode('utf-8')
    return async_response


def send_put_and_wait_for_response(cloud_api, channel_type, ep_id, apikey, resource_path, resource_data='120',
                                   timeout=30):
    """
    Send a put rest request to specific resource and wait for the async response from device
    :param resource_data: data to be updated at resource
    :param cloud_api:
    :param channel_type: websocket or callback
    :param ep_id: device id
    :param apikey:
    :param resource_path: path of the resource to device
    :param timeout: timeout for the async wait
    :return: dict / False
    """
    response = cloud_api.connect.set_device_resource(device_id=ep_id, resource_path=resource_path,
                                                     expected_status_code=202,
                                                     api_key=apikey, resource_data=resource_data)
    log.info('put initial response {}'.format(response))
    async_id = response.json()['async-response-id']
    # wait for async response
    async_response = channel_type.wait_for_async_response(async_response_id=async_id, timeout=timeout,
                                                          assert_errors=True)
    log.info('put async response {}'.format(async_response))
    return async_response


def send_post_and_wait_for_response(cloud_api, channel_type, ep_id, apikey, resource_path, resource_data="",
                                    timeout=30):
    """
    Send a post rest request to specific resource and wait for the async response from device.
    Empty post request can also be used to execute a function on device for example, registration update.
    Post with resource path will create that resource.
    :param cloud_api:
    :param channel_type: websocket or callback
    :param ep_id: device id
    :param apikey:
    :param resource_path: path of the resource to device
    :param resource_data: data which you want to send to resource, usually its empty to execute a function on device
    :param timeout: timeout for the async wait
    :return: dict / False
    """
    response = cloud_api.connect.create_device_resource(device_id=ep_id, resource_path=resource_path,
                                                        expected_status_code=202,
                                                        api_key=apikey, resource_data=resource_data)
    log.info('post initial response {}'.format(response))
    async_id = response.json()['async-response-id']
    # wait for async response
    async_response = channel_type.wait_for_async_response(async_response_id=async_id, timeout=timeout,
                                                          assert_errors=True)
    log.info('post async response {}'.format(async_response))
    return async_response


def send_del_and_wait_for_response(cloud_api, channel_type, ep_id, apikey, resource_path, timeout=30):
    """
    Send a delete rest request to specific resource and wait for the async response from device.
    Empty post request can also be used to remove (delete) a dynamic resource on the device.
    :param cloud_api:
    :param channel_type: websocket or callback
    :param ep_id: device id
    :param apikey:
    :param resource_path: path of the resource to device
    :param timeout: timeout for the async wait
    :return: dict / False
    """
    response = cloud_api.connect.remove_device_resource(device_id=ep_id, resource_path=resource_path,
                                                        expected_status_code=202,
                                                        api_key=apikey)
    log.info('delete initial response {}'.format(response))
    async_id = response.json()['async-response-id']
    # wait for async response
    async_response = channel_type.wait_for_async_response(async_response_id=async_id, timeout=timeout,
                                                          assert_errors=True)
    log.info('delete async response {}'.format(async_response))
    return async_response


def verify_cached_response_legacy(cloud_api, apikey, ep_id, resource_path, remaining_cache_time, expected_cached_value,
                                  expected_status_code=200):
    """
    The helper function to verify we are getting response value from cache not from device resource.
    :param expected_cached_value: the expected value from cache
    :param cloud_api:
    :param apikey:
    :param ep_id: endpoint of which we are testing the resource value
    :param remaining_cache_time: The remaining cache time for resource value in int
    :param resource_path: the resource path of which we want to check the value
    :param expected_status_code: the expected response code
    :return: true or assert failure.
    """

    assert remaining_cache_time > 0, 'resource max_age value is less than 1, so cannot start verifying cache resource'
    while remaining_cache_time > 0:
        cached_resp = cloud_api.connect.get_device_resources(device_id=ep_id, resource_path=resource_path,
                                                             expected_status_code=expected_status_code,
                                                             api_key=apikey)
        assert cached_resp.json() == expected_cached_value, 'did not get correct resource cached value'
        remaining_cache_time = int(cached_resp.headers.get('Cache-Control').split('=')[1])
        # wait for the next query approx 2 seconds till cache expire
        remaining_cache_time = remaining_cache_time - 2
        sleep(max(2, remaining_cache_time))
    return True
