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

"""
This module is for providing Izuma Cloud REST API functionalities
"""
from base64 import b64decode, b64encode

from izuma_systest_lib.cloud.libraries.billing import BillingAPI
from izuma_systest_lib.cloud.libraries.config_management import EdgeConfigManagementAPI
from izuma_systest_lib.cloud.libraries.connect import ConnectAPI
from izuma_systest_lib.cloud.libraries.device_directory import DeviceDirectoryAPI
from izuma_systest_lib.cloud.libraries.enrollment import EnrollmentAPI
from izuma_systest_lib.cloud.libraries.fcu import FcuAPI
from izuma_systest_lib.cloud.libraries.gateway_logs import GatewayLogsAPI
from izuma_systest_lib.cloud.libraries.iam import IamAPI
from izuma_systest_lib.cloud.libraries.rest_api.rest_api import RestAPI
from izuma_systest_lib.cloud.libraries.statistics import StatisticsAPI
from izuma_systest_lib.cloud.libraries.update import UpdateAPI
import logging


def decode_payload(payload):
    return b64decode(payload).decode('utf8')


def encode_payload(payload):
    return str(b64encode(payload.encode('utf-8')), 'utf-8')


log = logging.getLogger(__name__)


class IzumaCloud:
    """
    Izuma Cloud class to provide handles for all rest api libraries
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
