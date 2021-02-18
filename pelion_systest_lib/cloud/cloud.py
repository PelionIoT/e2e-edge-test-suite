"""
This module is for providing Pelion Cloud REST API functionalities
"""
from base64 import b64decode, b64encode

from pelion_systest_lib.cloud.libraries.admin import AdminAPI
from pelion_systest_lib.cloud.libraries.billing import BillingAPI
from pelion_systest_lib.cloud.libraries.config_management import EdgeConfigManagementAPI
from pelion_systest_lib.cloud.libraries.connect import ConnectAPI
from pelion_systest_lib.cloud.libraries.device_directory import DeviceDirectoryAPI
from pelion_systest_lib.cloud.libraries.enrollment import EnrollmentAPI
from pelion_systest_lib.cloud.libraries.fcu import FcuAPI
from pelion_systest_lib.cloud.libraries.gateway_logs import GatewayLogsAPI
from pelion_systest_lib.cloud.libraries.iam import IamAPI
from pelion_systest_lib.cloud.libraries.rest_api.rest_api import RestAPI
from pelion_systest_lib.cloud.libraries.statistics import StatisticsAPI
from pelion_systest_lib.cloud.libraries.update import UpdateAPI
import logging


def decode_payload(payload):
    return b64decode(payload).decode('utf8')


def encode_payload(payload):
    return str(b64encode(payload.encode('utf-8')), 'utf-8')

log = logging.getLogger(__name__)


class PelionCloud:
    """
    Pelion Cloud class to provide handles for all rest api libraries
    :param cloud_config_data: Cloud config data object
    """

    def __init__(self, cloud_config_data):
        # Rest API client for the cloud's API subdomain
        self._rest_api = RestAPI(cloud_config_data)
        self._rest_api_gateways = None
        self._rest_api_edge_k8s = None

        # Only initialize a rest client for these domains if the key is provided
        if 'gateways_url' in cloud_config_data:
            # Rest API client for the cloud's gateways subdomain
            self._rest_api_gateways = RestAPI(cloud_config_data, 'gateways_url')

        if 'edge_k8s_url' in cloud_config_data:
            # Rest API client for the cloud's edge-k8s subdomain
            self._rest_api_edge_k8s = RestAPI(cloud_config_data, 'edge_k8s_url')

        self._admin = AdminAPI(self.rest_api)
        self._billing = BillingAPI(self.rest_api)
        self._connect = ConnectAPI(self.rest_api)
        self._device_directory = DeviceDirectoryAPI(self.rest_api)
        self._enrollment = EnrollmentAPI(self.rest_api)
        self._fcu = FcuAPI(self.rest_api)
        self._iam = IamAPI(self.rest_api)
        self._statistics = StatisticsAPI(self.rest_api)
        self._update = UpdateAPI(self.rest_api)
        self._config_management = EdgeConfigManagementAPI(self.rest_api)
        self._gateway_logs = GatewayLogsAPI(self.rest_api)

    @property
    def rest_api(self):
        """
        Returns RestAPI class
        """
        return self._rest_api

    @property
    def rest_api_gateways(self):
        """
        Returns RestAPI class for gateways subdomain
        """
        return self._rest_api_gateways

    @property
    def rest_api_edge_k8s(self):
        """
        Returns RestAPI class edge-k8s subdomain
        """
        return self._rest_api_edge_k8s

    @property
    def admin(self):
        """
        Returns AdminAPI class
        """
        return self._admin

    @property
    def billing(self):
        """
        Returns BillingAPI class
        """
        return self._billing

    @property
    def connect(self):
        """
        Returns ConnectAPI class
        """
        return self._connect

    @property
    def device_directory(self):
        """
        Returns DeviceDirectoryAPI class
        """
        return self._device_directory

    @property
    def enrollment(self):
        """
        Returns EnrollmentAPI class
        """
        return self._enrollment

    @property
    def fcu(self):
        """
        Returns FcuAPI class
        """
        return self._fcu

    @property
    def iam(self):
        """
        Returns IamAPI class
        """
        return self._iam

    @property
    def statistics(self):
        """
        Returns StatisticsAPI class
        """
        return self._statistics

    @property
    def update(self):
        """
        Returns UpdateAPI class
        """
        return self._update

    @property
    def config_management(self):
        """
        Returns config management API class
        """
        return self._config_management

    @property
    def gateway_logs(self):
        """
        Returns gateway logs API class
        """
        return self._gateway_logs

    def reset(self, device_id, channel, async_id=None):
        """
        Reset device
        :param edge_internal_id: Get internal id
        :param channel: Webhook / callback api
        :param async_id: Async id if predefined
        :param
        """
        log.info('Factory reset. Device: {}'.format(device_id))
        self.post_and_wait('/3/0/5', None, device_id, channel, 200, async_id)

    def reboot(self, device_id, websocket, async_id=None):
        """
        Reboot device
        :param device_id: device internal id
        :param channel: Webhook / callback api
        :param async_id: Async id if predefined
        :return:
        """
        log.info('Reboot. Device: {}'.format(device_id))
        self.post_and_wait('/3/0/4', None, device_id, websocket, 200, async_id)


    @staticmethod
    def wait_registration(device_id, websocket, timeout=300):
        """
        Wait device registration from given channel
        :param edge_internal_id: device internal id
        :param channel: callback / websocket fixture
        :return:
        """
        data = websocket.wait_for_registration(device_id=device_id, timeout=timeout)
        if data:
            log.info('Registration notification received from channel for device: {}'.format(data))

        assert data is not False, 'Registration notification not received after ' \
                                  'reboot by timeout: {}'.format(timeout)
