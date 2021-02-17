"""
Edge Base connection, which is base for all kind of edge connections

Configuration values:

"""
import json
import logging
from time import time, sleep

from pelion_systest_lib.cloud.edge_cloud import PelionEdgeCloud
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
        self._internal_id = self.internal_id_configuration_value

        self.connector = self.get_connector_instance(self.connection_type, tc_config_data)

    def get_connector_instance(self, connection_type, tc_config_data):
        if connection_type == 'cloud': # pylint: disable=no-else-return
            return AbstractConnector()
        elif connection_type == 'local':
            return LocalConnection(self, tc_config_data)
        elif connection_type == 'remote_terminal':
            return RemoteTerminalConnection(tc_config_data)
        else:
            raise AssertionError('Connection type not cloud, local or remote_terminal. Check your configuration file.')


    def connect_protocol_translator(self):
        """
        Connecting protocol translator and return url for it
        Raise exception if not possible
        :return: protocol translator url
        """
        url = self.edge_core_url
        if not url:
            url = self.connector.connect_protocol_translator(self.edge_core_socket_path)
        # Put ending part of address
        url = self._get_pt_address(url)
        log.debug('Protocol translator socket available in {}'.format(url))
        return url

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
        if self.skip_release:
            log.debug('Skipping release')
            self.connector.skip_release()
        else:
            log.debug('Releasing edge connection')
            try:
                if self.is_developer_mode:
                    log.debug('Deleting developer devices..')
                    edge_cloud_api = PelionEdgeCloud(self.tc_config_data)
                    edge_cloud_api.delete_edge_devices(self.internal_id)
                    edge_cloud_api.delete_edge(self.internal_id)
            except BaseException as e:
                log.warning('Something went wrong in device deleting: {}'.format(e))
            finally:
                self.connector.release()


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
            url=RemoteTerminal.get_wss_address(self.api_gw, self.internal_id)
        ).execute_command(command)

    @property
    def internal_id(self):
        """
        Read internal_id from fastest place
        :return:
        """
        if self._internal_id:
            source = 'object'
            if self._internal_id == self.internal_id_configuration_value:
                source = 'configuration'
            log.debug('Internal_id: {} (source: {})'.format(self._internal_id, source))
            return self._internal_id
        return self.read_internal_id()

    @property
    def is_preinstalled(self):
        """ Internal id in configuration means that device is already installed """
        if bool(self.internal_id_configuration_value):
            return True

        log.debug('No internal_id in configuration, try to read status api..')
        try:
            self.read_internal_id()
            return True
        except:  # pylint: disable=bare-except
            log.debug('Cannot read internal_id from status api')
        log.debug('Edge is not installed')
        return False

    @property
    def ip_address(self):
        return self.connector.ip_address

    @property
    def has_remote_terminal(self):
        return self.tc_config_data.get('has_remote_terminal', True)

    def is_connected(self, timeout=120):
        # Edge may need some time for setup in very weak AWS machines
        status = self.read_status_api_with_retry(timeout=timeout)
        if status:
            return status.get('status') == 'connected'
        return False

    def wait_for_connected(self, timeout=120):
        """ In case internal id in configuration then we might not be able to read status api"""
        if bool(self.internal_id_configuration_value):
            return True

        log.debug('Wait for edge to be connected..')
        timeout_start = time()
        while time() < timeout_start + timeout:
            # Check connected multiple time during the waiting..
            if self.is_connected(timeout=int(timeout / 5)):
                log.info('Edge is successfully connected')
                return True
            sleep(5)
        raise Exception('Edge cannot connect to the cloud!')


    def read_status_api_with_retry(self, timeout=10):
        start_time = time()
        while True:
            try:
                return self.read_status_api()
            except Exception:  # pylint: disable=broad-except
                log.debug('Cannot read status api, trying again..')

            if time() - start_time > timeout:
                raise Exception('Timeout: Cannot read status api in {} seconds'.format(timeout))
            sleep(1)  # Sleep a bit to avoid busy loop

    def read_status_api(self):
        """
        Read status api and return dict
        :return:
        """
        response = self.execute_command('curl {}'.format(self.status_api_address))
        log.debug('edge-core status-api response: {}'.format(response))
        try:
            response = response[response.find('{'):(response.find('}') + 1)]
            json_dump = json.dumps(response)
            json_content = json.loads(json_dump)
            status_json = json.loads(json_content)
            log.debug('Edge status: {}'.format(status_json))
            return status_json
        except Exception as err:  # pylint: disable=broad-except
            log.error('Unable to read status api content. Edge not running? Content: {}, Error: {}'.format(
                response, err))

        raise Exception('Cannot read edge-core status api!')

    def read_internal_id(self, timeout=60):
        """
        Read internal ID from status api
        :return:
        """

        # Sometimes internal id is empty and need to loop couple of times to get real value
        start_time = time()
        while time() < start_time + timeout:
            internal_id = self.read_status_api().get('internal-id')
            if internal_id:
                log.debug('Internal_id: {} (source: status api)'.format(internal_id))
                self._internal_id = internal_id
                return internal_id
            log.debug('No internal_id available yet.. trying again..')
            sleep(1)  # Sleep a bit to avoid busy loop

        raise Exception('Timeout: Cannot read internal_id in {} seconds'.format(timeout))
