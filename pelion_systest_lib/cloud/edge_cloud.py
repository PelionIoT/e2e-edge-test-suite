import base64
import json
import logging
from time import time, sleep

from pelion_systest_lib.cloud.cloud import PelionCloud
from pelion_systest_lib.cloud.connect_handler import send_async_device_and_wait_for_response
from pelion_systest_lib.cloud.libraries.rest_api.rest_api import RestAPI

log = logging.getLogger(__name__)


class PelionEdgeCloud(PelionCloud):
    """ Pelion cloud api which contains edge helper function """

    def __init__(self, cloud_config_data):
        # Define pelion cloud super class
        PelionCloud.__init__(self, cloud_config_data)


    def get_endpoint_id(self, edge_internal_id, endpoint_name, timeout=30):

        query_params = {'limit': '1000', 'include': 'total_count',
                        'filter': 'host_gateway__eq={}'.format(edge_internal_id)}

        timeout_start = time()
        while time() < timeout_start + timeout:
            r = self.device_directory.get_devices(query_params, expected_status_code=200)
            endpoint_list = json.loads(r.text).get('data')
            for endpoint in endpoint_list:
                if endpoint.get('endpoint_name') == endpoint_name:
                    return endpoint.get('id')
            sleep(0.5)
        raise Exception('Cannot find endpoint {} connected to device {}'.format(endpoint_name, edge_internal_id))

    @staticmethod
    def payload_to_b64(value):
        return str(base64.b64encode(str(value).encode()), 'utf-8')

    def put_and_wait(self, uri, value, device_id, channel, async_id=None):
        """
        Make PUT request for Pelion cloud
        :param uri: resource url
        :param value: new value for put
        :param device_id: Device id in Pelion
        :param channel: Notification channel if needed
        :param async_id: Async id if predefined
        :return:
        """

        payload = {'method': 'PUT', 'uri': uri, }
        if value:
            payload['payload-b64'] = self.payload_to_b64(value)

        return send_async_device_and_wait_for_response(self, channel_type=channel,
                                                       ep_id=device_id,
                                                       apikey=channel.api_key,
                                                       payload=payload, async_id=async_id)

    def post_and_wait(self, uri, value, device_id, channel, expected_status_code=None, async_id=None):
        payload = {'method': 'POST', 'uri': uri, }
        if value:
            payload['payload-b64'] = self.payload_to_b64(value)

        resp = send_async_device_and_wait_for_response(self, channel_type=channel,
                                                       ep_id=device_id,
                                                       apikey=channel.api_key,
                                                       payload=payload, async_id=async_id)

        if expected_status_code:
            assert resp and resp['status'] == expected_status_code, 'Post to {} resource value failed'.format(uri)

        return resp

    def reset(self, edge_internal_id, channel, async_id=None):
        """
        Reset device
        :param edge_internal_id: Get internal id
        :param channel: Webhook / callback api
        :param async_id: Async id if predefined
        :param
        """
        log.info('Factory reset. Device: {}'.format(edge_internal_id))
        self.post_and_wait('/3/0/5', None, edge_internal_id, channel, 200, async_id)

    def reboot(self, edge_internal_id, channel, async_id=None):
        """
        Reboot device
        :param edge_internal_id: Get internal id
        :param channel: Webhook / callback api
        :param async_id: Async id if predefined
        :return:
        """
        log.info('Reboot. Device: {}'.format(edge_internal_id))
        self.post_and_wait('/3/0/4', None, edge_internal_id, channel, 200, async_id)


    @staticmethod
    def wait_registration(edge_internal_id, channel, timeout=300):
        """
        Wait device registration from given channel
        :param edge_internal_id: device internal id
        :param channel: callback / websocket fixture
        :return:
        """
        data = channel.wait_for_registration(device_id=edge_internal_id, timeout=timeout)
        if data:
            log.info('Registration notification received from channel for device: {}'.format(data))

        assert data is not False, 'Registration notification not received after ' \
                                  'reboot by timeout: {}'.format(timeout)

    def get_connected_devices(self, edge_internal_id):
        """
        List edge connected devices
        :param edge_internal_id: Edge internal id
        :return list of edge connected devices
        """
        query_params = {'limit': '1000', 'include': 'total_count', 'filter': 'host_gateway={}'.format(edge_internal_id)}

        resp = self.device_directory.get_devices(query_params, expected_status_code=200)

        device_list = []
        content = json.loads(resp.text)
        data = content.get('data')
        for item in data:
            endpoint_id = item.get('id')
            device_list.append(endpoint_id)

        return device_list

    def delete_edge_devices(self, edge_internal_id):
        """
        Delete edge connected devices from cloud
        :param edge_internal_id: internal id of host device
        :param delete_edge: True/False
        :return: -
        """
        device_list = self.get_connected_devices(edge_internal_id)

        for device_id in device_list:
            log.info('Deleting device id: {}'.format(device_id))
            self.device_directory.delete_device(device_id)

    def delete_edge(self, edge_internal_id):
        """
        Delete edge from cloud
        :param edge_internal_id: internal id of host device
        :return: -
        """
        log.info('Deleting edge device id: {}'.format(edge_internal_id))
        self.device_directory.delete_device(edge_internal_id)
