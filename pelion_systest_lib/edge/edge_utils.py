"""
Edge related helper functions
"""

import json
import logging
import time

import pytest

log = logging.getLogger(__name__)


class EdgeUtils:
    """
    Edge utilities class
    """
    tc_config = None
    tc_attribute_config = None
    _device_attributes = None
    gateway_devices = {}

    log = logging.getLogger(__name__)

    @staticmethod
    def _read_status_api(_, edge):
        return edge.read_status_api()

    @staticmethod
    def _read_internal_id(_, edge):
        return edge.read_internal_id()

    @staticmethod
    def is_connected(_, edge):
        return edge.is_connected()

    @staticmethod
    def wait_for_connected(_, edge, timeout=90):
        edge.wait_for_connected(timeout)

    @staticmethod
    def get_internal_id(tc_config_data, edge, assert_in_failure=False, timeout=90):
        """
        Get DUT internal id based on configuration
        :param tc_config_data: Test case config
        :param edge: Edge connection
        :param assert_in_failure. assert if internal id not known
        :param timeout
        :return: DUT internal id
        """
        internal_id = tc_config_data.get('internal_id')
        if internal_id:
            return internal_id

        # Try to get internal ID in loop
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            internal_id = edge.read_internal_id()
            if internal_id:
                break
            time.sleep(0.25)  # Not to be too aggressive

        if assert_in_failure and internal_id is None:
            assert False, \
                'Device internal id not known. Possible configuration error or internal id cannot be read from device'
        else:
            log.info('Internal id: {}'.format(internal_id))

        return internal_id

    @staticmethod
    def status_api(_, edge):
        return edge.read_status_api()

    @staticmethod
    def execute_command(_, edge, command):
        return edge.execute_command(command, wait_output=2, timeout=120)


    @staticmethod
    def skip_case(internal_id):
        """
        Skip case
        :param internal_id:
        """
        if not internal_id:
            log.info('Edge internal id unknown. Skipping test case')
            pytest.skip()

    def attribute_configuration(self, tc_config_data):
        """
        Save attributes from configuration for later use in test cases
        :param tc_config_data: Test case config
        """
        self.tc_attribute_config = tc_config_data.get('attributes')
        return self.tc_attribute_config if self.tc_attribute_config else dict()

    def device_attributes(self, cloud_api, internal_id):
        """
        Save attributes from device for later use in test cases
        :param cloud_api
        :param internal_id: Device internal id
        """
        r = cloud_api.device_directory.get_device(internal_id, expected_status_code=200)
        self._device_attributes = json.loads(r.text)
        return self._device_attributes

    @property
    def attributes(self):
        """
        Get attributes
        :return: device attributes list
        """
        return self._device_attributes

    def gateway_connected_devices(self, cloud_api, internal_id):
        """
        Save attributes from device for later use in test cases
        :param cloud_api
        :param internal_id: Edge internal id stored as dict key
        """
        query_params = {'limit': '1000', 'include': 'total_count', 'filter': 'host_gateway={}'.format(internal_id)}

        r = cloud_api.device_directory.get_devices(query_params, expected_status_code=200)

        connected_devices = []
        content = json.loads(r.text)
        data = content.get('data')
        for item in data:
            endpoint_id = item.get('id')
            connected_devices.append(endpoint_id)

        self.gateway_devices[internal_id] = connected_devices

        return self.gateway_devices[internal_id]




