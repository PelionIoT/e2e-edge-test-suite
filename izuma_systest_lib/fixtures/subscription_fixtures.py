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

"""
Subscriptions related pytest fixtures
"""

import logging
import pytest


log = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def subscribe_to_resource(cloud_api, new_temp_test_case_developer_api_key):
    """
    Subscribe to resource fixture
    """
    subscriptions = []

    def subscribe(resource_path):
        """
        Presubscribe to resource
        :param resource_path: Path to resource to subscribe
        """
        # Add subscription
        data = [{'resource-path': [resource_path]}]
        cloud_api.connect.set_pre_subscriptions(subscription_data=data, api_key=new_temp_test_case_developer_api_key,
                                                expected_status_code=204)
        subscriptions.append(resource_path)

    yield subscribe

    # Remove subscriptions
    cloud_api.connect.remove_pre_subscriptions(api_key=new_temp_test_case_developer_api_key, expected_status_code=204)
