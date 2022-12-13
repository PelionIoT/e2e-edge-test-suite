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
# This test file test(s) use Izuma device management device directory API's
# to get device information e.g. device attributes like registration status.
#
# More details about device-directory API's:
# https://developer.izumanetworks.com/docs/device-management-api/device-directory/
# ----------------------------------------------------------------------------
import logging
import pytest

log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def device_attributes(cloud_api, edge):
    attributes = cloud_api.device_directory.get_device(edge.device_id, expected_status_code=200).json()
    for key in attributes:
        log.info('\t{} : {}'.format(key, attributes[key]))

    yield attributes


def test_device_registered(cloud_api, edge, device_attributes):
    assert device_attributes['state'] == 'registered'
