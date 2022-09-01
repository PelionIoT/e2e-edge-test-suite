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

import logging

log = logging.getLogger(__name__)


class EdgeConfig:

    def __init__(self, tc_config_data):
        log.debug('Initializing edge config')
        self.tc_config_data = tc_config_data
        self.connection_type = tc_config_data.get('connection_type')
        log.debug('connection_type: {}'.format(self.connection_type))

    @property
    def has_remote_terminal(self):
        return self.tc_config_data.get('has_remote_terminal', True)

    @property
    def api_key(self):
        return self.tc_config_data['api_key']

    @property
    def api_gw(self):
        return self.tc_config_data['api_gw']

    @property
    def device_id_configuration_value(self):
        return self.tc_config_data.get('device_id', None)
