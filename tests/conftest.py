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
import uuid

import pytest

pytest_plugins = [
    'pelion_systest_lib.fixtures.edge_fixtures',
    'pelion_systest_lib.fixtures.general_fixtures',
    'pelion_systest_lib.fixtures.iam_fixtures',
    'pelion_systest_lib.fixtures.notification_fixtures',
    'pelion_systest_lib.fixtures.subscription_fixtures'
]

log = logging.getLogger(__name__)

pytest.global_test_results = []


def pytest_addoption(parser):
    """
    Function for pytest to enable own custom commandline arguments
    :param parser: argparser
    :return:
    """
    parser.addoption('--config_path', action='store', help='Test case config json')
    parser.addoption('--show_api_key', action='store', help='true/false to show api keys on logs')
    parser.addoption('--no_summary', action='store_true', help='Does not collect the test result summary')