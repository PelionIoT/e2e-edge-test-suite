"""
This module is for cloud's Connect API functions
"""
from base64 import b64encode
import pelion_systest_lib.tools as utils


class ConnectAPI:
    """
    A class that provides Device management connect related functionality.
    https://www.pelion.com/docs/device-management/current/service-api-references/device-management-connect.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Device Management Connect library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v2'
        self.cloud_api = rest_api

    def register_callback_url(self, webhook_data, api_key=None, expected_status_code=None):
        """
        Register callback url
        :param webhook_data: {"url": [callback_url], "headers": {"authorization": "xxxx"}}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /v2/notification/callback response
        """
        api_url = '/{}/notification/callback'.format(self.api_version)

        r = self.cloud_api.put(api_url, api_key, webhook_data, expected_status_code=expected_status_code)
        return r

    def get_callback_url(self, api_key=None, expected_status_code=None):
        """
        Get callback url
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v2/notification/callback response
        """
        api_url = '/{}/notification/callback'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def delete_callback_url(self, api_key=None, expected_status_code=None):
        """
        Delete callback url
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v2/notification/callback response
        """
        api_url = '/{}/notification/callback'.format(self.api_version)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def send_async_request_to_device(self, device_id, request_data, async_id=None, retry_count=None,
                                     expiry_seconds=None, api_key=None, device_reference=None,
                                     expected_status_code=None):
        """
        Send async request to device. For normal simple use cases see self.async_request().
        :param device_id: Device id
        :param request_data: Request payload data
        :param async_id: Async id, required
        :param retry_count: Retry count
        :param expiry_seconds: Expiry timeout
        :param api_key: Authentication key
        :param device_reference: e.g. 'endpoint_name' when using endpoint_name as device id
        :param expected_status_code: Asserts the result in the function
        :return: POST /v2/device-requests/{device_id} response
        """
        api_url = '/{}/device-requests/{}'.format(self.api_version, device_id)

        assert async_id is not None, 'async_id is required parameter!'
        async_params = {'async-id': async_id}
        if retry_count is not None:
            async_params['retry'] = retry_count
        if expiry_seconds is not None:
            async_params['expiry-seconds'] = expiry_seconds
        if device_reference is not None:
            async_params['device_reference'] = device_reference

        r = self.cloud_api.post(api_url, api_key, request_data, params=async_params,
                                expected_status_code=expected_status_code)
        return r


    def get_pre_subscriptions(self, api_key=None, expected_status_code=None):
        """
        Get pre-subscriptions
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v2/subscriptions response
        """
        api_url = '/{}/subscriptions'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def set_pre_subscriptions(self, subscription_data=None, api_key=None, expected_status_code=None):
        """
        Set pre-subscriptions
        :param subscription_data: Pre-subscriptions payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /v2/subscriptions response
        """
        api_url = '/{}/subscriptions'.format(self.api_version)

        r = self.cloud_api.put(api_url, api_key, subscription_data, expected_status_code=expected_status_code)
        return r

    def remove_pre_subscriptions(self, api_key=None, expected_status_code=None):
        """
        Delete pre-subscriptions
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v2/subscriptions response
        """
        api_url = '/{}/subscriptions'.format(self.api_version)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_endpoints_subscriptions(self, device_id, api_key=None, expected_status_code=None):
        """
        Get endpoint's subscriptions
        :param device_id: Device id       :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v2/subscriptions/{device_id} response
        """
        api_url = '/{}/subscriptions/{}'.format(self.api_version, device_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def remove_endpoints_subscriptions(self, device_id, api_key=None, expected_status_code=None):
        """
        Remove endpoint's subscriptions
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v2/subscriptions/{device_id} response
        """
        api_url = '/{}/subscriptions/{}'.format(self.api_version, device_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_subscription_status(self, device_id, resource_path, api_key=None, expected_status_code=None):
        """
        Read subscription status
        :param device_id: Device id
        :param resource_path: Resource path
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v2/subscriptions/{device_id}/{resource_path} response
        """
        api_url = '/{}/subscriptions/{}/{}'.format(self.api_version, device_id, resource_path)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def set_subscription_for_resource(self, device_id, resource_path, api_key=None, expected_status_code=None):
        """
        Subscribe to resource path
        :param device_id: Device id
        :param resource_path: Resource path
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /v2/subscriptions/{device_id}/{resource_path} response
        """
        # Remove first "/" if already set
        resource_path = resource_path[1:] if resource_path.startswith('/') else resource_path
        api_url = '/{}/subscriptions/{}/{}'.format(self.api_version, device_id, resource_path)

        r = self.cloud_api.put(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def remove_subscription_from_resource(self, device_id, resource_path, api_key=None, expected_status_code=None):
        """
        Remove subscription from resource
        :param device_id: Device id
        :param resource_path: Resource path
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v2/subscriptions/{device_id}/{resource_path} response
        """
        api_url = '/{}/subscriptions/{}/{}'.format(self.api_version, device_id, resource_path)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def register_websocket_channel(self, api_key=None, expected_status_code=None, configuration=None):
        """
        Register websocket channel
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :param configuration: Special configuration object for notification service, see
            https://www.pelion.com/docs/device-management/current/service-api-references/notifications-api.html#registerWebhook
        :return: PUT /v2/notification/websocket response
        """
        api_url = '/{}/notification/websocket'.format(self.api_version)

        r = self.cloud_api.put(api_url, api_key, expected_status_code=expected_status_code, json=configuration)
        return r

    def get_websocket_channel(self, api_key=None, expected_status_code=None):
        """
        Get websocket channel info
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v2/notification/websocket response
        """
        api_url = '/{}/notification/websocket'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def delete_websocket_channel(self, api_key=None, expected_status_code=None):
        """
        Delete websocket channel
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v2/notification/websocket response
        """
        api_url = '/{}/notification/websocket'.format(self.api_version)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def register_data_management_channel(self, payload, api_key=None, expected_status_code=None):
        """
        Register Data Management Channel
        :param payload: e.g. {apikey: 80ee18bc-791b-4a42-acad-cafeabcd1234, database: db_name, tablename: table_name}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /v2/notification/datamanagement response
        """
        api_url = '/{}/notification/datamanagement'.format(self.api_version)

        r = self.cloud_api.put(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def get_data_management_channel(self, api_key=None, expected_status_code=None):
        """
        Get Data Management Channel
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v2/notification/datamanagement response
        """
        api_url = '/{}/notification/datamanagement'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def delete_data_management_channel(self, api_key=None, expected_status_code=None):
        """
        Delete Data Management Channel
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v2/notification/callback response
        """
        api_url = '/{}/notification/datamanagement'.format(self.api_version)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def change_resource_value(self, device_id, resource_path, value, api_key=None, expected_status_code=None):
        """
        Change resource value of the device
        :param device_id: device id
        :param resource_path: Path to resource value to be changed "/<object>/0/<resource>"
        :param value: Value to set in string format
        :param api_key: Api key to use in query
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-requests/{device_id} response
        """
        api_url = '/{}/device-requests/{}'.format(self.api_version, device_id)

        async_params = {'async-id': '{}-{}'.format(device_id, utils.build_random_string(6))}

        # Set payload
        payload_b64 = b64encode(value.encode('utf-8')).decode('utf-8')
        payload = {"method": "PUT", "uri": resource_path,
                   "accept": "text/plain",
                   "content-type": "text/plain",
                   "payload-b64": payload_b64}

        r = self.cloud_api.post(api_url, api_key, payload, params=async_params,
                                expected_status_code=expected_status_code)
        return r

    def get_device_echo(self, device_id, api_key=None, expected_status_code=None):
        """
        Get device resources from echo
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /v3/devices/{device_id}/echo
        """
        api_url = '/v3/devices/{}/echo'.format(device_id)
        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def delete_device_echo(self, device_id, api_key=None, expected_status_code=None):
        """
        Delete device echo data
        :param device_id: Device id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /v3/devices/{device_id}/echo
        """
        api_url = '/v3/devices/{}/echo'.format(device_id)
        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def async_request(self, device_id, resource, async_id=None, method='GET', payload=None, accept='text/plain',
                      content_type='text/plain', api_key=None):
        """
        Helper to send async request to the device without complex payload building

        :param device_id: Device ID as 01751b38556200000000000100108a2f
        :param resource: Resource path as /3201/0/5853
        :param async_id: Async_ID string or None when random string will be used
        :param method: GET/PUT/POST/DELETE, defaults to GET
        :param payload: Payload string
        :param accept: The content type that the requesting client will accept
        :param content_type: Describes the content type of the base-64 encoded payload-b64 field
        :param api_key: Specific API key or None when one from config will be used
        :return: async_id used to do the request

        Examples:
            r = cloud_api.connect.async_request('01751b38556200000000000100108a2f', '/3201/0/5853')
            r = cloud_api.connect.async_request('01751b38556200000000000100108a2f', '/3201/0/5853', method='PUT',
                                                payload='1:2:3:4')
        """

        # This looks stupid. Payload is given as a string, b64encode takes bytes and gives bytes though it is ascii
        # string, so it needs to be decoded back. For binary payload something else has to be invented but that's rare.
        # Payload is usually not given for GET, use try-catch to set it None.
        try:
            payload_b64 = b64encode(payload.encode('utf-8')).decode('utf-8')
        except AttributeError:
            payload_b64 = None
        request_data = {'method': method, 'uri': resource, 'payload-b64': payload_b64, 'accept': accept,
                        'content-type': content_type}
        if async_id is None:
            async_id = utils.build_random_string(5)
        self.send_async_request_to_device(device_id, request_data=request_data, async_id=async_id, api_key=api_key)
        return async_id
