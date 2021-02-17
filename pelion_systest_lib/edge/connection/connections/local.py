# pylint: disable=too-many-instance-attributes

import logging
import subprocess

from pelion_systest_lib.edge.connection.abstract_connector import AbstractConnector

log = logging.getLogger(__name__)


class LocalConnection(AbstractConnector):
    """
    Local connection class - overrides Abstract connection class
    """

    def __init__(self, connector, config):
        log.debug('LocalConnection')
        self.connector = connector
        self.edge_core_path = config.get('edge_core_path')
        self.edge_socket_path = config.get('edge_core_socket_path')

    def connect(self, timeout=10):
        return self

    def execute_command(self, command, wait_output=5, timeout=120):
        """ Execute command in local machine """
        log.info('Executing command: {}'.format(command))
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout is not None:
            stdout = stdout.decode(errors='ignore')
            log.info('stdout: {}'.format(stdout))
        if stderr is not None:
            stderr = stderr.decode(errors='ignore')
            log.info('stderr: {}'.format(stderr))

        # If only stderr has content, return it to make able assert error cases
        if not stdout and stderr:
            return stderr
        return stdout




