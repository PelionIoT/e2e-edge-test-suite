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

# pylint: disable=redefined-outer-name,bare-except,invalid-name
"""
Notification service related pytest fixtures
"""

import logging
import pytest
from izuma_systest_lib.cloud.websocket_handler import WebsSocketNotificationChannel

log = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def websocket(cloud_api, new_temp_test_case_developer_api_key, request):
    """
    WebSocket channel fixture. Configuration object for notification service can be delivered via fixture request
    parameter. https://www.pelion.com/docs/device-management/current/service-api-references/notifications-api.html#registerWebhook

    Example test code:
    CONFIG = {'serialization': {'type': 'v2', 'max_chunk_size': '100', 'cfg':
    {'deregistrations_as_object': 'false',
     'include_uid': 'true',
     'include_timestamp': 'true',
     'include_original_ep': 'true'
     }}}

    @pytest.mark.parametrize('websocket', [CONFIG], indirect=True)
    def test_01_websocket_v2(websocket, linux_fcu_client, cloud_api, new_temp_test_case_developer_api_key):
        ...
    """
    log.info('Register and open WebSocket notification channel')
    try:
        configuration = request.param
    except AttributeError:
        configuration = None

    ws = WebsSocketNotificationChannel(cloud_api, new_temp_test_case_developer_api_key, configuration)
    yield ws.handler
    ws.close()


@pytest.fixture(scope='module')
def websocket_for_module(cloud_api, new_temp_module_developer_api_key):
    """
    Module level WebSocket channel fixture
    """
    ws = WebsSocketNotificationChannel(cloud_api, new_temp_module_developer_api_key)
    yield ws.handler
    ws.close()


@pytest.fixture(scope='function')
def websocket_notification_channel(cloud_api, temp_access_key):
    """
    WebSocket channel fixture which uses temporary application and access key
    :return:
    """
    ws = WebsSocketNotificationChannel(cloud_api, temp_access_key())
    yield ws.handler
    ws.close()


@pytest.fixture(scope='module')
def websocket_notification_channel_for_module(cloud_api, temp_access_key):
    """
    WebSocket channel fixture which uses temporary application and access key
    :return:
    """
    ws = WebsSocketNotificationChannel(cloud_api, temp_access_key())
    yield ws.handler
    ws.close()
