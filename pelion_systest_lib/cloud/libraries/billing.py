"""
This module is for cloud's Billing API functions
"""


class BillingAPI:
    """
    A class that provides Billing related functionality.
    https://www.pelion.com/docs/device-management/current/service-api-references/billing.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Connect statistics library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v3'
        self.cloud_api = rest_api

    def get_billing_report(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get billing report
        :param query_params: {'month': '2019-03'}
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /billing-report response
        """
        api_url = '/{}/billing-report'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_billing_report_active_devices(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get raw billing data of the active devices for the month
        :param query_params: {'month': '2019-03'}
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /billing-report-active-devices response
        """
        api_url = '/{}/billing-report-active-devices'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_billing_report_firmware_updates(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get raw billing data of the firmware updates for the month
        :param query_params: {'month': '2019-03'}
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /billing-report-firmware-updates response
        """
        api_url = '/{}/billing-report-firmware-updates'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_service_packages_quota(self, api_key=None, expected_status_code=None):
        """
        Get service package quota
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /service-packages-quota response
        """
        api_url = '/{}/service-packages-quota'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_service_packages_quota_history(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get service package quota history
        :param query_params: e.g.{'limit': '1000'}
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /service-packages-quota-history response
        """
        api_url = '/{}/service-packages-quota-history'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_service_packages(self, api_key=None, expected_status_code=None):
        """
        Get service packages
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /service-packages response
        """
        api_url = '/{}/service-packages'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_billing_statistics(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get statistics view of Device Management usage  in time series
        :param query_params: e.g. {'interval': '2h', 'period': '2d'}
        :param api_key: Authentication token (API key or Authorization token)
        :param expected_status_code: Asserts the result in the function
        :return: GET /billing-statistics response
        """
        api_url = '/{}/billing-statistics'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r
