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
This module is for cloud's Statistics API functions
"""


class StatisticsAPI:
    """
    A class that provides Connect statistics related functionality.
    https://www.pelion.com/docs/device-management/current/service-api-references/connect-statistics.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Connect statistics library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v3'
        self.cloud_api = rest_api

    def get_metrics(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get account specific statistics
        :param query_params: e.g.{'include': ['transactions', 'total_count']}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-images response
        """
        api_url = '/{}/metrics'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r
