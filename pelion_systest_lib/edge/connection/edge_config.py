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
    def internal_id_configuration_value(self):
        return self.tc_config_data.get('internal_id', None)

    def get_provisioning_mode(self):
        return self.tc_config_data.get('edge_provisioning_mode', 'developer')

    @property
    def skip_release(self):
        return self.tc_config_data.get('edge_skip_release', False)

    @property
    def edge_core_url(self):
        return self.tc_config_data.get('edge_core_url', None)

    @property
    def is_factory_mode(self):
        return self.get_provisioning_mode() == 'factory'

    @property
    def is_developer_mode(self):
        return self.get_provisioning_mode() == 'developer'


    @property
    def status_api_port(self):
        return self.tc_config_data.get('edge_local_host_port')

    @property
    def status_api_address(self):
        return 'localhost:{}/status'.format(self.status_api_port)

    @property
    def edge_core_socket_path(self):
        path = self.tc_config_data.get('edge_core_socket_path', None)
        if path:
            log.debug('Edge core path: {} (source: configuration)'.format(path))
            return path

        raise Exception('Edge-core path is not defined!')

    def get_protocol_translator_address(self):
        url = self.tc_config_data.get('edge_core_url', None)
        if url:
            log.debug('Edge core url: {} (source: configuration)'.format(url))
            return self._get_pt_address(url)

        raise Exception('Edge-core configuration error: "edge_core_url" not defined in configuration')
