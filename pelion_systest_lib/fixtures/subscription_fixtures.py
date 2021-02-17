"""
Subscriptions related pytest fixtures
"""

import logging
from time import sleep

import pytest

import pelion_systest_lib.helpers.r__client as client_helper

log = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def subscription(get_linux_client_with_dynamic_observable_aob_objects_resources,
                 new_temp_module_developer_api_key, cloud_api, notification_channel_for_module):
    """
    Fixture to subscribe for a provided list in the parameters like [[obs_res_name, obs_obj_ins_name, obs_obj_name]]
    :param get_linux_client_with_dynamic_observable_aob_objects_resources:
    :param new_temp_module_developer_api_key:
    :param cloud_api:
    :param notification_channel_for_module:
    :return:
    """
    _, _, _, ep_id = get_linux_client_with_dynamic_observable_aob_objects_resources
    resource_paths = []

    def set_subscription(resources):
        for res_path in resources:
            resp = cloud_api.connect.set_subscription_for_resource(ep_id, resource_path='{}'.format(res_path),
                                                                   expected_status_code=202,
                                                                   api_key=new_temp_module_developer_api_key)
            assert notification_channel_for_module.wait_for_async_response(
                assert_errors=True, async_response_id=resp.json()['async-response-id'])['status'] == 200, \
                'Failed to subscribe for the resource'
            resource_paths.append(res_path)

    yield set_subscription

    for resource_path in resource_paths:
        cloud_api.connect.remove_subscription_from_resource(ep_id, '{}'.format(resource_path), expected_status_code=204,
                                                            api_key=new_temp_module_developer_api_key)


@pytest.fixture(scope='module')
def set_pre_subscriptions(request, get_linux_client_with_dynamic_observable_aob_objects_resources,
                          new_temp_module_developer_api_key, cloud_api):
    """
    Fixture to presubscribe for a provided list in the parameters like
    [{'resource-path': [aobs_res_name]}, {'resource-path': [aobs_obj_ins_name]}, {'resource-path': [aobs_obj_name]}]
    :param request:
    :param get_linux_client_with_dynamic_observable_aob_objects_resources:
    :param new_temp_module_developer_api_key:
    :param cloud_api:
    :return:
    """
    data = request.param()
    cloud_api.connect.set_pre_subscriptions(data, expected_status_code=204, api_key=new_temp_module_developer_api_key)
    _, _, linux_client, _ = get_linux_client_with_dynamic_observable_aob_objects_resources
    client_helper.send_to_client(linux_client, 'cloud-client keep_alive')
    # sleep time for presubscription to get effective
    sleep(10)
    yield
    cloud_api.connect.remove_pre_subscriptions(expected_status_code=204, api_key=new_temp_module_developer_api_key)


@pytest.fixture(scope='function')
def subscribe_to_resource(cloud_api, new_temp_test_case_developer_api_key):
    """
    Subscribe to resource fixture
    """
    subscriptions = []

    def subscribe(resource_path):
        """
        Presubscribe to resource
        :param resource_path: Path to resource to subscribe
        """
        # Add subscription
        data = [{'resource-path': [resource_path]}]
        cloud_api.connect.set_pre_subscriptions(subscription_data=data, api_key=new_temp_test_case_developer_api_key,
                                                expected_status_code=204)
        subscriptions.append(resource_path)

    yield subscribe

    # Remove subscriptions
    cloud_api.connect.remove_pre_subscriptions(api_key=new_temp_test_case_developer_api_key, expected_status_code=204)
