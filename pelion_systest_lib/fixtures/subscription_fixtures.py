"""
Subscriptions related pytest fixtures
"""

import logging
from time import sleep

import pytest


log = logging.getLogger(__name__)


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
