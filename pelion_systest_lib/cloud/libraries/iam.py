# ----------------------------------------------------------------------------
# Copyright (c) 2020-2021, Pelion and affiliates.
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

# pylint: disable=too-many-public-methods
"""
This module is for cloud's IAM API functions
"""

import logging
import os

import pelion_systest_lib.tools as utils

log = logging.getLogger(__name__)


class IamAPI:
    """
    A class that provides IAM related functionality.
    https://www.pelion.com/docs/device-management/current/service-api-references/account-management.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Iam library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v3'
        self.cloud_api = rest_api

    def login_user(self, account, username, password, expected_status_code=None):
        """
        User login
        :param account: Account id
        :param username: Username
        :param password: Password
        :param expected_status_code: Asserts the result in the function
        :return: Login info
        """
        r = self.cloud_api.login(account, username, password, expected_status_code=expected_status_code)
        return r

    def logout_user(self, api_key=None, expected_status_code=None):
        """
        User Logout
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return:
        """
        r = self.cloud_api.logout(api_key, expected_status_code=expected_status_code)
        return r

    def create_account(self, account_info=None, api_key=None, expected_status_code=None):
        """
        Create a new account (tier 0 by default)
        :param account_info: Account info payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /accounts response
        """
        random_str = utils.build_random_string(10)

        api_url = '/{}/accounts'.format(self.api_version)
        payload = {
            "tier": "0",
            "display_name": "SystestCompanyOy",
            "admin_name": random_str,
            "company": "SystestCompanyOy",
            "country": "Finland",
            "state": "Pohjois-Pohjanmaa",
            "address_line1": "Torikatu 18B",
            "address_line2": "Floor 3-5",
            "postal_code": "90100",
            "city": "Oulu",
            "admin_email": "testuser199+{}@systest-emailserver-789877574.eu-west-1.elb.amazonaws.com".format(
                random_str),
            "email": "testuser199+{}@systest-emailserver-789877574.eu-west-1.elb.amazonaws.com".format(random_str),
            "end_market": "Agriculture",
            "aliases": ["SystestCompanyOy_{}".format(random_str)]
        }
        if account_info is not None:
            payload = account_info

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def delete_account(self, account_id, api_key=None, expected_status_code=None):
        """
        Delete the defined account
        :param account_id: Account id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /account/{account_id} response
        """
        api_url = '/{}/accounts/{}'.format(self.api_version, account_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_account(self, account_id=None, api_key=None, expected_status_code=None):
        """
        Get the account info
        :param account_id: Account id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /accounts/{account_id} response (if account id defined)
        :return: GET /accounts/me response (if account id not defined)
        """
        if account_id is None:
            api_url = '/{}/accounts/me'.format(self.api_version)
        else:
            api_url = '/{}/accounts/{}'.format(self.api_version, account_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_accounts(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get all accounts
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /accounts response
        """
        api_url = '/{}/accounts'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def update_account(self, account_id, new_account_data, api_key=None, expected_status_code=None):
        """
        Update the account info
        :param account_id: Account id
        :param new_account_data: New account data payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /accounts/{account_id} response
        """
        api_url = '/{}/accounts/{}'.format(self.api_version, account_id)

        r = self.cloud_api.put(api_url, api_key, new_account_data, expected_status_code=expected_status_code)
        return r

    def create_trusted_certificate(self, cert_data, api_key=None, expected_status_code=None):
        """
        Create a new certificate
        :param cert_data: Certificate payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /trusted-certificates response
        """
        api_url = '/{}/trusted-certificates'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, cert_data, expected_status_code=expected_status_code)
        return r

    def delete_trusted_certificate(self, cert_id, api_key=None, expected_status_code=None):
        """
        Delete trusted certificate
        :param cert_id: Certificate id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /trusted-certificates/{cert_id} response
        """
        api_url = '/{}/trusted-certificates/{}'.format(self.api_version, cert_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_trusted_certificates(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get certificates
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /trusted-certificates response
        """
        api_url = '/{}/trusted-certificates'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def update_trusted_certificate(self, cert_id, cert_data, api_key=None, expected_status_code=None):
        """
        Update trusted certificate
        :param cert_id: Certificate id
        :param cert_data: Certificate payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /trusted-certificates/{cert_id} response
        """
        api_url = '/{}/trusted-certificates/{}'.format(self.api_version, cert_id)

        r = self.cloud_api.put(api_url, api_key, cert_data, expected_status_code=expected_status_code)
        return r

    def create_developer_certificate(self, cert_data, api_key=None, expected_status_code=None):
        """
        Create a new developer certificate
        :param cert_data: Certificate payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /developer-certificates response
        """
        api_url = '/{}/developer-certificates'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, cert_data, expected_status_code=expected_status_code)
        return r

    def get_developer_certificate(self, certificate_id, api_key=None, expected_status_code=None):
        """
        Get developer certificate
        :param certificate_id: Developer certificate id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /developer-certificates/{certificate_id} response
        """
        api_url = '/{}/developer-certificates/{}'.format(self.api_version, certificate_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_policy_groups(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get policy groups
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /policy-groups response
        """
        api_url = '/{}/policy-groups'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def create_policy_group(self, policy_group_data, api_key=None, expected_status_code=None):
        """
        Create a new policy group
        :param policy_group_data: Policy group payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /policy-groups response
        """
        api_url = '/{}/policy-groups'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, policy_group_data, expected_status_code=expected_status_code)
        return r

    def delete_policy_group(self, policy_group_id, api_key=None, expected_status_code=None):
        """
        Delete a  policy group
        :param policy_group_id: Policy group id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /policy-groups response
        """
        api_url = '/{}/policy-groups/{}'.format(self.api_version, policy_group_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_user(self, user_info=None, root_user=False, api_key=None, expected_status_code=None):
        """
        Create a new user
        :param user_info: Override the 'default' generated user info
        :param root_user: Set true if creating root user
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /users response
        """
        random_str = utils.build_random_string(10)

        if root_user:
            api_url = '/{}/accounts/%2F/users'.format(self.api_version)
        else:
            api_url = '/{}/users'.format(self.api_version)

        payload = {'username': 'syte_fute_user_{}'.format(random_str),
                   'full_name': random_str,
                   'email': "testuser199+{}@systest-emailserver-789877574.eu-west-1.elb.amazonaws.com".format(
                       random_str),
                   'address': 'Torikatu, Oulu, 90100, Finland',
                   'phone_number': '+123456789'}
        if root_user:
            payload['username'] = 'syte_fute_root_user_{}'.format(random_str)
        if user_info is not None:
            payload = user_info

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def delete_user(self, user_id, root_user=False, api_key=None, expected_status_code=None):
        """
        Delete the defined user
        :param user_id: User id
        :param root_user: Set true if deleting root user
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /users/{user_id} response
        """
        if root_user:
            api_url = '/{}/accounts/%2F/users/{}'.format(self.api_version, user_id)
        else:
            api_url = '/{}/users/{}'.format(self.api_version, user_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_user(self, user_id, api_key=None, expected_status_code=None):
        """
        Get the user info
        :param user_id: User id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /users/{user_id} response
        """
        api_url = '/{}/users/{}'.format(self.api_version, user_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_users(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get all users
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /users response
        """
        api_url = '/{}/users'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def update_user(self, user_id, new_user_data, root_user=False, api_key=None, expected_status_code=None):
        """
        Update the user info
        :param user_id: User id
        :param new_user_data: New user data payload
        :param root_user: Set true if root user
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /users/{user_id} response
        """
        if root_user:
            api_url = '/{}/accounts/%2F/users/{}'.format(self.api_version, user_id)
        else:
            api_url = '/{}/users/{}'.format(self.api_version, user_id)
        payload = new_user_data

        r = self.cloud_api.put(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def update_user_password(self, user_id, new_password, api_key=None, root_user=False, expected_status_code=None):
        """
        Update the user password
        :param api_key: Authentication key
        :param user_id: User id
        :param new_password: New password string
        :param root_user: Set true if root user
        :param expected_status_code: Asserts the result in the function
        :return: PUT /users/{user_id} response
        """
        if root_user:
            api_url = '/{}/accounts/%2F/users/{}/password'.format(self.api_version, user_id)
        else:
            api_url = '/{}/users/{}'.format(self.api_version, user_id)
        payload = {'password': new_password}

        r = self.cloud_api.put(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def create_api_key(self, api_key_group_id, api_key=None, expected_status_code=None):
        """
        Generate API key
        :param api_key: Authentication key
        :param api_key_group_id: Group id
        :param expected_status_code: Asserts the result in the function
        :return: POST /api-key response
        """
        api_url = '/{}/api-keys'.format(self.api_version)
        payload = {'name': 'Syte_dynamic_{}_API_key'.format(os.getenv('JOB_NAME', 'local')[:70]),
                   'groups': [api_key_group_id]}

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def get_api_key(self, api_key_id, api_key=None, expected_status_code=None):
        """
        Get the api key info
        :param api_key_id: Api key id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /api-keys/{api_key_id} response
        """
        api_url = '/{}/api-keys/{}'.format(self.api_version, api_key_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_api_keys(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get list of API keys
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /api-keys response
        """
        api_url = '/{}/api-keys'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def update_api_key(self, api_key_id, api_key_data, api_key=None, expected_status_code=None):
        """
        Update api key details
        :param api_key_id: Api key id
        :param api_key_data: Api key payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /api-keys/{cert_id} response
        """
        api_url = '/{}/api-keys/{}'.format(self.api_version, api_key_id)

        r = self.cloud_api.put(api_url, api_key, api_key_data, expected_status_code=expected_status_code)
        return r

    def delete_api_key(self, api_key_id, api_key=None, expected_status_code=None):
        """
        Delete the defined API key
        :param api_key_id: API key id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /api-keys/{api key_id} response
        """
        api_url = '/{}/api-keys/{}'.format(self.api_version, api_key_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_agreements(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get agreements
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /agreements response
        """
        api_url = '/{}/agreements'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_signed_agreements(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get signed agreements
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /signed-agreements response
        """
        api_url = '/{}/signed-agreements'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def accept_signed_agreement(self, agreement_id, api_key=None, expected_status_code=None):
        """
        Accept signed agreement
        :param agreement_id: Agreement id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /signed-agreements response
        """
        api_url = '/{}/signed-agreements'.format(self.api_version)
        payload = {'agreement_id', agreement_id}

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def get_server_credentials(self, mode='bootstrap', api_key=None, expected_status_code=None):
        """
        Get server credentials
        :param mode: bootstrap / lwm2m
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /server-credentials/{mode} response
        """
        api_url = '/{}/server-credentials/{}'.format(self.api_version, mode)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_all_server_credentials(self, api_key=None, expected_status_code=None):
        """
        Get all server credentials
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /server-credentials response
        """
        api_url = '/{}/server-credentials'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def authenticate_user(self, account, username, password, expected_status_code=None):
        """
        Authenticates user by executing login
        :param account: Account id
        :param username: Username
        :param password: Password
        :param expected_status_code: Asserts the result in the function
        :return: Login response
        """
        r = self.cloud_api.login(account=account, username=username, password=password,
                                 expected_status_code=expected_status_code)
        return r

    def get_or_create_policy_group(self, group_name='Developers'):
        """
        Get policy group by name or create new one if not exists yet
        :param group_name: Policy group name. Developers is default value
        :return: policy group id
        """

        # Check if policy group exists already
        resp = self.get_policy_groups(expected_status_code=200).json()
        for group in resp['data']:
            if group['name'] == group_name:
                return group['id']

        # Group did not exist, then creating new one
        r = self.create_policy_group(
            policy_group_data={'name': group_name},
            expected_status_code=200)
        return r.json()['id']

    def get_or_create_application(self, application_name=None, group_ids=None, access_key=None,
                                  group_name='Developers'):
        """
        Check if application exists and create new one if don't exist yet
        :param application_name: Name of the application
        :param group_ids: Application groups if need to create new one
        :param group_name: Used security group name if group_id is not known
        :param access_key: Access key used for requests
        :return: application key
        """

        if application_name is None:
            application_name = 'Syte_{}_application'.format(os.getenv('JOB_NAME', 'manual_test')[:70])

        if group_ids is None:
            group_ids = self.get_or_create_policy_group(group_name)

        applications = self.get_applications(access_key, 200).json()['data']
        for application in applications:
            if application['name'] == application_name:
                return application['id']

        app_id = self.create_application(application_name, group_ids, access_key, 201).json()['id']
        log.info('Created new application name: {}, id: {}'.format(application_name, app_id))
        return app_id

    def create_application(self, application_name, group_ids=None, access_key=None, expected_status_code=None):
        """
        Create a new application
        :param application_name: Application name
        :param group_ids: string or string array of groups for application
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /applications response
        """

        api_url = '/{}/applications'.format(self.api_version)

        groups = [group_ids] if isinstance(group_ids, str) else group_ids
        payload = {'name': application_name, 'groups': groups}

        return self.cloud_api.post(api_url, access_key, payload, expected_status_code=expected_status_code)

    def get_application(self, application_id, access_key=None, expected_status_code=None):
        """
        Get application details
        :param application_id: Application ID
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /applications/{application_id} response
        """
        api_url = '/{}/applications/{}'.format(self.api_version, application_id)

        r = self.cloud_api.get(api_url, access_key, expected_status_code=expected_status_code)
        return r

    def update_application(self, application_id, application_data, access_key=None, expected_status_code=None):
        """
        Update application
        :param application_id: Application ID
        :param application_data: New application attributes data
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /application/{application_id} response
        """

        api_url = '/{}/applications/{}'.format(self.api_version, application_id)

        r = self.cloud_api.put(api_url, access_key, application_data, expected_status_code=expected_status_code)
        return r

    def delete_application(self, application_id, access_key=None, expected_status_code=None):
        """
        Delete application
        :param application_id: Application ID
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /applications/{application_id} response
        """
        api_url = '/{}/applications/{}'.format(self.api_version, application_id)

        r = self.cloud_api.delete(api_url, access_key, expected_status_code=expected_status_code)
        return r

    def get_applications(self, access_key=None, expected_status_code=None):
        """
        Get all applications
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /applications response
        """
        api_url = '/{}/applications'.format(self.api_version)

        return self.cloud_api.get(api_url, access_key, expected_status_code=expected_status_code)

    def create_access_key(self, application_id, access_key_name=None, access_key=None, expected_status_code=None):
        """
        Generate access key
        :param application_id: Application ID
        :param access_key_name: Name for access key
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /applications/{application_id}/access-keys response
        """
        api_url = '/{}/applications/{}/access-keys'.format(self.api_version, application_id)
        if access_key_name is None:
            temp_name = 'local_{}'.format(utils.build_random_string(5, use_digits=True))
            access_key_name = 'Syte_dynamic_{}_access_key'.format(os.getenv('JOB_NAME', temp_name)[:70])
        payload = {'name': access_key_name}

        r = self.cloud_api.post(api_url, access_key, payload, expected_status_code=expected_status_code)
        return r

    def get_access_key(self, application_id, access_key_id, access_key=None, expected_status_code=None):
        """
        Get access key details
        :param application_id: Application ID
        :param access_key_id: Access key ID
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /applications/{application_id}/access-keys/{access_key_id} response
        """
        api_url = '/{}/applications/{}/access-keys/{}'.format(self.api_version, application_id, access_key_id)

        r = self.cloud_api.get(api_url, access_key, expected_status_code=expected_status_code)
        return r

    def update_access_key(self, application_id, access_key_id, access_key_data, access_key=None,
                          expected_status_code=None):
        """
        Update access_key
        :param application_id: Application ID
        :param access_key_id: Access key ID
        :param access_key_data: New access key attributes data
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /application/{application_id}/access-keys/{access_key_id} response
        """

        api_url = '/{}/applications/{}/access-keys/{}'.format(self.api_version, application_id, access_key_id)

        r = self.cloud_api.put(api_url, access_key, access_key_data, expected_status_code=expected_status_code)
        return r

    def delete_access_key(self, application_id, access_key_id, access_key=None, expected_status_code=None):
        """
        Delete access key
        :param application_id: Application ID
        :param access_key_id: Access key ID
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /applications/{application_id}/access-keys/{access_key_id} response
        """
        api_url = '/{}/applications/{}/access-keys/{}'.format(self.api_version, application_id, access_key_id)

        r = self.cloud_api.delete(api_url, access_key, expected_status_code=expected_status_code)
        return r

    def get_access_keys(self, application_id, access_key=None, expected_status_code=None):
        """
        Get all access keys of application
        :param application_id: Application ID
        :param access_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /applications/{application_id}/access-keys response
        """
        api_url = '/{}/applications/{}/access-keys'.format(self.api_version, application_id)

        r = self.cloud_api.get(api_url, access_key, expected_status_code=expected_status_code)
        return r
