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
