# ----------------------------------------------------------------------------
# Copyright (c) 2020-2021, Pelion and affiliates.
# Copyright (c) 2022, Izuma Networks
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

# pylint: disable=redefined-outer-name
"""
IAM test cases related pytest fixtures
"""

import logging
import os
import uuid

import pytest

import izuma_systest_lib.cloud.iam as iam_helpers
from izuma_systest_lib.cloud.libraries.access_key import TemporaryAccessKey

log = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def new_temp_test_case_developer_api_key(cloud_api):
    """
    Create new temporary function level developer api key
    :param cloud_api: Cloud API fixture
    :return: Rest API response for new developer api key
    """
    log.info('Creating new developer api key for test case')
    r = iam_helpers.create_api_key(cloud_api, 'Developers')
    resp = r.json()

    log.info('Created new developer api key for test case, id: {}'.format(resp['id']))

    yield resp['key']

    log.info('Cleaning out the generated test case developer api key, id: {}'.format(resp['id']))
    cloud_api.iam.delete_api_key(resp['id'], expected_status_code=204)


@pytest.fixture(scope='module')
def new_temp_module_developer_api_key(cloud_api):
    """
    Create new temporary module level developer api key
    :param cloud_api: Cloud API fixture
    :return: Rest API response for new developer api key
    """
    log.info('Creating new developer api key for test case')
    r = iam_helpers.create_api_key(cloud_api, 'Developers')
    resp = r.json()

    log.info('Created new developer api key for test module, id: {}'.format(resp['id']))

    yield resp['key']

    log.info('Cleaning out the generated test module developer api key, id: {}'.format(resp['id']))
    cloud_api.iam.delete_api_key(resp['id'], expected_status_code=204)


def application_scope(fixture_name, config):  # pylint: disable=unused-argument
    return os.environ.get('application_scope', 'module')


@pytest.fixture(scope=application_scope)
def temp_application(cloud_api):
    """
    Create new temporary application
    Example of the fixture call: temp_application_id = temp_application('Developers')
    :return: function for creating temporary application
    """
    application_ids = []

    def create_application(group='Developers'):
        """
        Actual creation part
        :param group: Existing group name
        :return: application id
        """
        log.info('Creating new {} application'.format(group.lower()))
        application_name = 'Syte_{creator}_{random_part}_app'.format(
            creator=os.getenv('JOB_NAME', 'manual'),
            random_part=str(uuid.uuid4())[-10:])

        app_id = cloud_api.iam.create_application(
            application_name=application_name,
            group_ids=cloud_api.iam.get_or_create_policy_group(group),
            expected_status_code=201).json()['id']

        log.info('Created new application with name: {}, id: {}'.format(application_name, app_id))
        application_ids.append(app_id)
        return app_id

    yield create_application

    for app_id in application_ids:
        log.info('Cleaning out the generated application, id: {}'.format(app_id))
        cloud_api.iam.delete_application(app_id, expected_status_code=204)


@pytest.fixture(scope='session')
def application(cloud_api, tc_config_data):
    """
    Get test application or create new one if not exists yet
    :param cloud_api: Cloud api object
    :param tc_config_data: Test configuration as map
    :return: application id
    """
    return tc_config_data.get('application_id', cloud_api.iam.get_or_create_application())


def access_key_scope(fixture_name, config):  # pylint: disable=unused-argument
    return os.environ.get('access_key_scope', 'module')


@pytest.fixture(scope=access_key_scope)
def temp_access_key(cloud_api, temp_application):
    """
    Create new temporary access_key using also temporary application
    Example of the fixture call: temp_key = temp_access_key('Developers')
    :param cloud_api: Cloud API fixture
    :param temp_application: temporary application create function
    :return: Rest API response for new access key
    """
    temp_keys = list()

    def create_access_key(group='Developers'):
        """
        Create temporary access key for temporary application
        :param group: User group for application
        :return: access key
        """
        temp_key = TemporaryAccessKey(cloud_api, temp_application(group))
        temp_keys.append(temp_key)
        return temp_key.key

    yield create_access_key

    for temp_key in temp_keys:
        temp_key.delete()
