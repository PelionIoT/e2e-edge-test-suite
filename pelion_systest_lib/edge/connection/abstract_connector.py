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

# pylint: disable=no-self-use
"""
Define connector interface
"""
import logging
from abc import abstractmethod

log = logging.getLogger(__name__)


class AbstractConnector:

    @abstractmethod
    def connect(self, timeout=10):
        """ Connect the computer"""

    def reboot(self):
        raise Exception('Cannot reboot with this configuration')

    @abstractmethod
    def release(self):
        """
        Release resource
        """

    @abstractmethod
    def execute_command(self, command, wait_output=5, timeout=120):
        """
        Makes a connection to the device under test
        :param command: command to be send
        :param wait_output: delay in seconds how long response will be waited
        :return: output as string
        """
