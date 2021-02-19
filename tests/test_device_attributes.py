import logging
import pytest


log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def device_attributes(cloud_api, edge):
    response = cloud_api.device_directory.get_device(edge.device_id, expected_status_code=200).json()
    yield response


def test_list_attributes(cloud_api, edge, device_attributes):
    log.info('Device: {} attributes'.format(edge.device_id))
    for key in device_attributes:
        log.info('{} : {}'.format(key, device_attributes[key]))


def test_device_registered(cloud_api, edge, device_attributes):
    assert device_attributes['state'] == 'registered'

