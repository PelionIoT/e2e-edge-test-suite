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
