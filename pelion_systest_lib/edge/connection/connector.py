"""
Edge Base connection, which is base for all kind of edge connections

Configuration values:

"""
import logging
from time import time, sleep

from pelion_systest_lib.edge.connection.abstract_connector import AbstractConnector
from pelion_systest_lib.edge.connection.edge_config import EdgeConfig
from pelion_systest_lib.edge.connection.connections.local import LocalConnection
from pelion_systest_lib.edge.connection.connections.remote_terminal import RemoteTerminalConnection
from pelion_systest_lib.edge.remote_terminal import RemoteTerminal

log = logging.getLogger(__name__)


class EdgeConnector(EdgeConfig):
    """
    Super class of connections
    """

    def __init__(self, tc_config_data):
        super().__init__(tc_config_data)

        log.debug('Initializing edge connector')
        self._device_id = self.device_id_configuration_value

        self.connector = self.get_connector_instance(self.connection_type, tc_config_data)

    def get_connector_instance(self, connection_type, tc_config_data):
        if connection_type == 'cloud':  # pylint: disable=no-else-return
            return AbstractConnector()
        elif connection_type == 'local':
            return LocalConnection(self, tc_config_data)
        elif connection_type == 'remote_terminal':
            return RemoteTerminalConnection(tc_config_data)
        else:
            raise AssertionError('Connection type not cloud, local or remote_terminal. Check your configuration file.')

    def connect_edge(self):
        """
        Makes everything ready for edge testing
        """
        log.debug('Connecting edge..')
        self.connect()

        return self

    def connect(self, timeout=10):
        self.connector.connect(timeout=timeout)

    def reboot(self):
        self.connector.reboot()

    def release(self):
        pass

    def execute_command(self, command, wait_output=5, timeout=120):
        """
        :param command:
        :param wait_output: waiting output in case of RaaS
        :param timeout: Timeout for ssh command
        :return:
        """
        return self.connector.execute_command(command, wait_output, timeout)

    def execute_remote_terminal(self, command):
        return RemoteTerminal(
            api_key=self.api_key,
            url=RemoteTerminal.get_wss_address(self.api_gw, self.device_id)
        ).execute_command(command)

    @property
    def device_id(self):
        """
        Read device_id from configuration
        :return:
        """

        return self._device_id

    @property
    def has_remote_terminal(self):
        return self.tc_config_data.get('has_remote_terminal', True)
