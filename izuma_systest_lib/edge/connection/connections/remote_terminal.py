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

from izuma_systest_lib.edge.connection.abstract_connector import AbstractConnector
from izuma_systest_lib.edge.remote_terminal import RemoteTerminal

log = logging.getLogger(__name__)


class RemoteTerminalConnection(AbstractConnector):
    """
    Local connection class - overrides Abstract connection class
    """

    def __init__(self, config):
        log.debug('LocalConnection')

        if 'device_id' not in config.keys():
            raise Exception('device_id is missing from configuration. RemoteTerminalConnection cannot install edge!')

        self.remote_terminal = RemoteTerminal(
            api_key=config['api_key'],
            url=RemoteTerminal.get_wss_address(config['api_gw'], config.get('device_id'))
        )

    def connect(self, timeout=10):
        return self

    def release(self):
        pass

    def execute_command(self, command, wait_output=5, timeout=120):
        return self.remote_terminal.execute_command(command, timeout)
