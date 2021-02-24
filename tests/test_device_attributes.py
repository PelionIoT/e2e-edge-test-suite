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

import logging
import pytest

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@pytest.fixture(scope="module")
def device_attributes(cloud_api, edge):
    yield cloud_api.device_directory.get_device(edge.device_id, expected_status_code=200).json()


def test_list_attributes(cloud_api, edge, device_attributes):
    log.info('Device: {} attributes:'.format(edge.device_id))
    for key in device_attributes:
        log.info('\t{} : {}'.format(key, device_attributes[key]))


def test_device_registered(cloud_api, edge, device_attributes):
    assert device_attributes['state'] == 'registered'
