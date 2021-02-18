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