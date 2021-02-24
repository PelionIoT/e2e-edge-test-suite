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


def test_remote_terminal(edge):
    if not edge.has_remote_terminal:
        pytest.skip('Skipping because build don\'t have remote terminal')

    response = None
    try:
        response = edge.execute_remote_terminal('date +%A')
    except BaseException as e:
        log.info('Cannot execute using remote terminal: {}'.format(e))

    weekdays = ['Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday']

    assert response in weekdays, 'Remote terminal connection not working correctly'
