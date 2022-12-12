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
# This test file test(s) are testing that device remote terminal is functional
# All edge/gateway devices may not have remote terminal supported.
# Use configuration file parameter: has_remote_terminal to define if test is
# part of the set.
#
# Information regarding remote terminal
# https://developer.izumanetworks.com/docs/device-management-edge/2.2/managing/gateway-terminal-service.html
# ----------------------------------------------------------------------------

import logging
import pytest

log = logging.getLogger(__name__)


def test_remote_terminal(edge):
    if not edge.has_remote_terminal:
        pytest.skip('Skipping because device don\'t have remote terminal supported.')

    assert 'something' == edge.execute_remote_terminal('echo something'), 'Remote terminal connection not working ' \
                                                                          'correctly'
