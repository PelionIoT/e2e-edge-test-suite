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

# pylint: disable=no-member,bare-except
import asyncio
import logging
import aiohttp

log = logging.getLogger(__name__)


class RemoteTerminal:

    loop = None     # For storing the event-loop

    def __init__(self, api_key, url):
        """
        :param api_key: Izuma access key (or API key)
        :param url: Remote terminal url
        """
        # Create loop explicitly, Python 3.10 warns, 3.11 stops working..
        if self.loop == None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            log.debug(f"RemoteTerminal __init__ self.loop created {self.loop}")

        self.api_key = api_key
        self.url = url

    @staticmethod
    def get_wss_address(api_gw, device_id):
        return '{api_gw}/v3alpha/devices/{device_id}/console'.format(
            api_gw=api_gw.replace('https', 'wss'),
            device_id=device_id
        )

    @staticmethod
    async def send_terminal(websocket, cmd, timeout=10):
        """
        Send command to the edge remote terminal using existing websocket connection
        :param websocket: aiohttp websocket connection
        :param cmd: command to be sent
        :param timeout: timeout in seconds
        :return: None
        """

        message_content = {
            'type': 'input',
            'payload': cmd + '\r'  # Add new line to make it execute the command
        }
        log.debug('Websocket message sending: {}'.format(message_content))
        try:
            await asyncio.wait_for(websocket.send_json(message_content), timeout)
        except asyncio.TimeoutError:
            raise Exception('Timeout: Cannot send command to the edge remote terminal')

    @staticmethod
    async def read_terminal(websocket, timeout=10):
        """
        Reading message from edge remote terminal using existing websocket connection
        :param websocket: aiohttp websocket connection
        :param timeout: timeout in seconds
        :return: Message, or None in case of timeout
        """
        try:
            ret = await asyncio.wait_for(websocket.receive_json(), timeout)
        except BaseException as e:
            log.debug(e, exc_info=True)
            log.debug('Cannot read anything from websocket in {} seconds'.format(timeout))
            return None
        log.debug('Websocket message received: {}'.format(ret))
        if 'payload' not in ret.keys():
            log.debug('Wrong message, do not include payload key')
            raise Exception('Wrong return message from edge remote terminal connection. Check debug logs!')
        return ret['payload']

    async def _execute_command_async(self, cmd, timeout=10):
        """
        Do not use this because this don't have timeout handling. Use execute_command_with_timeout_async() instead
        :param cmd: command to be sent to the device
        :param timeout: timeout in seconds
        :return:
        """
        log.debug('Starting remote terminal connection')
        session = aiohttp.ClientSession()
        headers = {"Sec-WebSocket-Protocol": "pelion_{}".format(self.api_key)}
        async with session.ws_connect(self.url, timeout=timeout, ssl=False, headers=headers) as websocket:
            cmd_start_text = await self.read_terminal(websocket)
            await self.send_terminal(websocket, cmd)

            # Receive messages in loop
            message = ''
            while True:
                message += await self.read_terminal(websocket, timeout)
                if cmd_start_text in message:
                    log.debug('Cmd completed, ending websocket reading..')
                    break

            log.debug('Raw message: {}'.format(message))
            message = message.replace(cmd, '').replace(cmd_start_text, '').strip()
            log.debug('Cleaned message: {}'.format(message))
            log.debug('Closing websocket')
            await websocket.close()
        await session.close()
        log.debug('Websocket connection closed')
        return message

    async def execute_command_with_timeout_async(self, cmd, timeout=10):
        """
        This send command to the Edge device via remote terminal connection
        This function handle timeout
        :param cmd: Command to be sent for device
        :param timeout: timeout in seconds
        :return: message from device
        """
        try:
            return await asyncio.wait_for(self._execute_command_async(cmd, timeout), timeout)
        except asyncio.TimeoutError:
            raise Exception('Edge remote terminal is too slow!')
        except BaseException as e:
            log.debug(e, exc_info=True)
            raise Exception('Something went wrong with edge remote terminal! Check debug logs.')

    def execute_command(self, cmd, timeout=60):
        """
        This send command to the Edge device via remote terminal connection
        :param cmd: Command to be sent for device
        :param timeout: timeout in seconds
        :return: message from device
        """
        ret = self.loop.run_until_complete(self.execute_command_with_timeout_async(cmd, timeout))
        return ret


def execute_command_on_gateway(edge, tc_config_data, command):
    """
    Function to execute command on gateway terminal
    :param edge: Edge instance internal ID
    :param tc_config_data: Configuration json content
    :param command: command which has to be executed as string
    :return: message from device terminal as string
    """
    gateway_resp = RemoteTerminal(
        api_key=tc_config_data['api_key'],
        url=RemoteTerminal.get_wss_address(tc_config_data['api_gw'], edge.device_id)
    ).execute_command(command)
    return gateway_resp
