"""
This module is for cloud's gateway logs API functions
"""


class GatewayLogsAPI:
    """
    A class that provides gateway logs.
    https://github.com/ArmMbedCloud/mbed-cloud-api-contract/blob/IOTCLOUDPR-2992/gateway/public/logs.yaml
    """

    def __init__(self, rest_api):
        """
        :param rest_api: REST API request object
        """
        self.cloud_api = rest_api
        self.api_version = 'v3'

    def get_spicfic_device_logs(self, device_id, api_key=None, query_params=None, expected_status_code=None):
        """
        Get specific device logs
        :param api_key: Pelion api key
        :param device_id: Edge instance internal ID
        :param expected_status_code: Asserts the result in the function
        :return: GET /v3/devices/{device_id}/logs response
        """
        api_url = '/{}/devices/{}/logs'.format(self.api_version, device_id)
        resp = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return resp

    def get_all_device_logs_with_filter(self, api_key=None, query_params=None, expected_status_code=None):
        """
        Get all devices logs
        :param api_key: Pelion api key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v3/device-logs response
        """
        api_url = '/{}/device-logs'.format(self.api_version)
        resp = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return resp

    def get_all_device_logs_with_device_log_id(self, log_id, api_key=None, expected_status_code=None):
        """
        Get all devices logs
        :param log_id: mUUID Entity ID for logs
        :param api_key: Pelion api key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v3/device-logs/{device_log_id} response
        """
        api_url = '/{}/device-logs/{}'.format(self.api_version, log_id)
        resp = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return resp
