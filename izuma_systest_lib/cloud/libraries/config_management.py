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
This module is for cloud's config management API functions
"""


class EdgeConfigManagementAPI:
    """
    A class that provides edge config management.
    https://github.com/PelionIoT/wigwag-cloud-relay-configs/blob/master/swagger.yaml
    """

    def __init__(self, rest_api):
        """
        :param rest_api: REST API request object
        """
        self.cloud_api = rest_api
        self.api_version = 'v3alpha'

    def get_edge_config(self, device_id, api_key=None, query_params=None, expected_status_code=None):
        """
        Get edge config
        :param api_key: Izuma access key (or API key)
        :param device_id: Edge instance internal ID
        :param query_params: {'limit': 5, 'order': 'DESC'}
        :param expected_status_code: Asserts the result in the function
        :return: GET /v3alpha/devices/{device-id}/configurations response
        """
        api_url = '/{}/devices/{}/configurations'.format(self.api_version, device_id)
        resp = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return resp

    def set_edge_config(self, device_id, api_key=None, db_name=None, data=None, expected_status_code=None):
        """
        SET edge config
        :param api_key: Izuma access key (or API key)
        :param device_id: Edge instance internal ID
        :param db_name: name of the configuration data
        :param data: JSON data for configuration
        :param expected_status_code: Asserts the result in the function
        :return: PUT /v3alpha/devices/{device-id}/configurations/{configuration_name} response
        """
        api_url = '/{}/devices/{}/configurations/{}'.format(self.api_version, device_id, db_name)
        resp = self.cloud_api.put(api_url, api_key, payload=data, expected_status_code=expected_status_code)
        return resp

    def delete_edge_config(self, device_id, api_key=None, db_name=None, expected_status_code=None):
        """
        DELETE edge config
        :param api_key: Izuma access key (or API key)
        :param device_id: Edge instance internal ID
        :param db_name: name of the configuration data
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v3alpha/devices/{device-id}/configurations/{configuration_name} response
        """
        api_url = '/{}/devices/{}/configurations/{}'.format(self.api_version, device_id, db_name)
        resp = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return resp
