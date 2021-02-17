"""
This module is for cloud's Factory Tool functions
"""


class FcuAPI:
    """
    A class that provides Factory Tool Download related functionality.

    """

    def __init__(self, rest_api):
        """
        Initializes the Factory Tool Download library
        :param rest_api: RestAPI object
        """
        self.cloud_api = rest_api

    def get_factory_tool_info(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get factory tool info
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /downloads/fcu/info response
        """
        api_url = '/downloads/fcu/info'

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_factory_tool_release_notes(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get factory tool release notes
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /downloads/fcu/release_notes response
        """
        api_url = '/downloads/fcu/release_notes'

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def download_factory_tool(self, api_key=None, expected_status_code=None):
        """
        Download factory tool
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /downloads/fcu/factory_configurator_utility.zip
        """
        api_url = '/downloads/fcu/factory_configurator_utility.zip'

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r
