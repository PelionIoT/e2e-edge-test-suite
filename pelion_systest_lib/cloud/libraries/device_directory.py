"""
This module is for cloud's Device Directory API functions
"""


class DeviceDirectoryAPI:
    """
    A class that provides Device catalog related functionality.
    https://www.pelion.com/docs/device-management/current/service-api-references/device-directory.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Device Directory library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v3'
        self.cloud_api = rest_api

    def create_device(self, device_data, api_key=None, expected_status_code=None):
        """
        Create a device
        :param device_data: Device data payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /devices response
        """
        api_url = '/{}/devices'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, device_data, expected_status_code=expected_status_code)
        return r

    def delete_device(self, device_id, api_key=None, expected_status_code=None):
        """
        Delete the defined device
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /devices/{device_id} response
        """
        api_url = '/{}/devices/{}'.format(self.api_version, device_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_device(self, device_id, api_key=None, expected_status_code=None):
        """
        Get one device with device_id
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /devices/{device_id} response
        """
        api_url = '/{}/devices/{}'.format(self.api_version, device_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_devices(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get all devices
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /devices response
        """
        api_url = '/{}/devices'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def suspend_device(self, device_id, block, api_key=None, expected_status_code=None):
        """
        Suspend a device
        :param device_id: Device id
        :param block: Suspension block
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /devices/{device_id}/suspend response
        """

        api_url = '/{}/devices/{}/suspend'.format(self.api_version, device_id)

        r = self.cloud_api.post(api_url, api_key, block, expected_status_code=expected_status_code)
        return r

    def resume_device(self, device_id, block, api_key=None, expected_status_code=None):
        """
        Resume a device
        :param device_id: Device id
        :param block: Suspension block
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /devices/{device_id}/resume response
        """

        api_url = '/{}/devices/{}/resume'.format(self.api_version, device_id)

        r = self.cloud_api.post(api_url, api_key, block, expected_status_code=expected_status_code)
        return r

    def update_device_info(self, device_id, new_device_info, api_key=None, expected_status_code=None):
        """
        Update the device info
        :param device_id: Device id
        :param new_device_info: New device data payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /devices/{device_id} response
        """
        api_url = '/{}/devices/{}'.format(self.api_version, device_id)

        r = self.cloud_api.put(api_url, api_key, new_device_info, expected_status_code=expected_status_code)
        return r

    def get_device_events(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get device events
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-events response
        """
        api_url = '/{}/device-events'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def create_device_query(self, device_query_data, api_key=None, expected_status_code=None):
        """
        Create a device query
        :param device_query_data: Device query payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-queries response
        """
        api_url = '/{}/device-queries'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, device_query_data, expected_status_code=expected_status_code)
        return r

    def get_device_queries(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get device queries
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-queries response
        """
        api_url = '/{}/device-queries'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def update_device_query(self, device_query_id, device_query_data, api_key=None, expected_status_code=None):
        """
        Update device query
        :param device_query_id: Device query id
        :param device_query_data: Device query payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /device-queries response
        """
        api_url = '/{}/device-queries/{}'.format(self.api_version, device_query_id)

        r = self.cloud_api.put(api_url, api_key, device_query_data, expected_status_code=expected_status_code)
        return r

    def delete_device_query(self, device_query_id, api_key=None, expected_status_code=None):
        """
        Delete the defined device query
        :param device_query_id: Device query id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /device-queries/{device_query_id} response
        """
        api_url = '/{}/device-queries/{}'.format(self.api_version, device_query_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_device_group(self, device_group_data, api_key=None, expected_status_code=None):
        """
        Create a device group
        :param device_group_data: Device group payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-groups response
        """
        api_url = '/{}/device-groups'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, device_group_data, expected_status_code=expected_status_code)
        return r

    def delete_device_group(self, device_group_id, api_key=None, expected_status_code=None):
        """
        Delete the defined device group
        :param device_group_id: Device group id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /device-groups/{device_group_id} response
        """
        api_url = '/{}/device-groups/{}'.format(self.api_version, device_group_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_device_group(self, device_group_id, api_key=None, expected_status_code=None):
        """
        Get one device group with device_group_id
        :param device_group_id: Device group id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-groups/{device_group_id} response
        """
        api_url = '/{}/device-groups/{}'.format(self.api_version, device_group_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_device_groups(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get all device groups
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-groups response
        """
        api_url = '/{}/device-groups'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def update_device_group(self, device_group_id, device_group_data, api_key=None, expected_status_code=None):
        """
        Update device group
        :param device_group_id: Device group id
        :param device_group_data: Device group payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /device-groups/{device_group_id} response
        """
        api_url = '/{}/device-groups/{}'.format(self.api_version, device_group_id)

        r = self.cloud_api.put(api_url, api_key, device_group_data, expected_status_code=expected_status_code)
        return r

    def add_device_to_device_group(self, device_group_id, device_id, api_key=None, expected_status_code=None):
        """
        Add device to device group
        :param device_group_id: Device group id
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-groups/{device_group_id}/devices/add response
        """
        api_url = '/{}/device-groups/{}/devices/add'.format(self.api_version, device_group_id)
        payload = {"device_id": device_id}

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def get_devices_from_device_group(self, device_group_id, api_key=None, expected_status_code=None):
        """
        Get devices from device group
        :param device_group_id: Device group id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-groups/{device_group_id}/devices/ response
        """
        api_url = '/{}/device-groups/{}/devices/'.format(self.api_version, device_group_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def remove_device_from_device_group(self, device_group_id, device_id, api_key=None, expected_status_code=None):
        """
        Remove device from device group
        :param device_group_id: Device group id
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-groups/{device_group_id}/devices/remove response
        """
        api_url = '/{}/device-groups/{}/devices/remove'.format(self.api_version, device_group_id)
        payload = {"device_id": device_id}

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def get_device_block_categories(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get Device block categories
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-block-categories response
                """
        api_url = '/{}/device-block-categories'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r
