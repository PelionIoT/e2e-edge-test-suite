import logging

from pelion_systest_lib.edge.connection.abstract_connector import AbstractConnector
from pelion_systest_lib.edge.remote_terminal import RemoteTerminal

log = logging.getLogger(__name__)


class RemoteTerminalConnection(AbstractConnector):
    """
    Local connection class - overrides Abstract connection class
    """

    def __init__(self, config):
        log.debug('LocalConnection')

        if 'internal_id' not in config.keys():
            raise Exception('internal_id is missing from configuration. RemoteTerminalConnection cannot install edge!')

        self.remote_terminal = RemoteTerminal(
            api_key=config['api_key'],
            url=RemoteTerminal.get_wss_address(config['api_gw'], config.get('internal_id'))
        )

    def connect(self, timeout=10):
        return self

    def release(self):
        pass

    def execute_command(self, command, wait_output=5, timeout=120):
        return self.remote_terminal.execute_command(command, timeout)
