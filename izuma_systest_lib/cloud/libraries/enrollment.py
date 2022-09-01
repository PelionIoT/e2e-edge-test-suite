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

"""
This module is for cloud's Enrollment API functions
"""

import izuma_systest_lib.tools as utils


class EnrollmentAPI:
    """
    A class that provides Enrollment service related functionality, device and certificate
    https://www.pelion.com/docs/device-management/current/service-api-references/enrollment-api.html
    https://www.pelion.com/docs/device-management/current/service-api-references/certificate-enrollment.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Enrollment API library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v3'
        self.cloud_api = rest_api

    def get_device_enrollments(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get device enrollments
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-enrollments response
        """
        api_url = '/{}/device-enrollments'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_device_enrollment(self, enrollment_id, api_key=None, expected_status_code=None):
        """
        Get device enrollment
        :param enrollment_id: Enrollment id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-enrollments/{enrollment_id} response
        """
        api_url = '/{}/device-enrollments/{}'.format(self.api_version, enrollment_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_device_enrollment(self, enrollment_data=None, api_key=None, expected_status_code=None):
        """
        Create device enrollment
        :param enrollment_data: Enrollment payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-enrollments response
        """
        api_url = '/{}/device-enrollments'.format(self.api_version)
        payload = {"enrollment_identity": utils.build_random_enrollment_identity()}
        if enrollment_data is not None:
            payload = enrollment_data

        r = self.cloud_api.post(api_url, api_key, payload, expected_status_code=expected_status_code)
        return r

    def delete_device_enrollment(self, enrollment_id, api_key=None, expected_status_code=None):
        """
        Delete device enrollment
        :param enrollment_id: Enrollment id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /device-enrollments/{enrollment_id} response
        """
        api_url = '/{}/device-enrollments/{}'.format(self.api_version, enrollment_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_bulk_enrollment_upload(self, enrollment_identities, api_key=None, expected_status_code=None):
        """
        Bulk enrollment upload
        :param enrollment_identities: Enrollment csv
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-enrollments-bulk-uploads response
        """
        api_url = '/{}/device-enrollments-bulk-uploads'.format(self.api_version)
        files = {'enrollment_identities': enrollment_identities}

        r = self.cloud_api.post(api_url, api_key, files=files, expected_status_code=expected_status_code)
        return r

    def get_bulk_enrollment_upload(self, enrollment_id, api_key=None, expected_status_code=None):
        """
        Get bulk enrollment upload
        :param enrollment_id: Enrollment id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-enrollments-bulk-uploads/{enrollment_id} response
        """
        api_url = '/{}/device-enrollments-bulk-uploads/{}'.format(self.api_version, enrollment_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_bulk_enrollment_delete(self, enrollment_id, api_key=None, expected_status_code=None):
        """
        Get bulk enrollment delete
        :param enrollment_id: Enrollment id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /device-enrollments-bulk-deletes/{enrollment_id} response
        """
        api_url = '/{}/device-enrollments-bulk-deletes/{}'.format(self.api_version, enrollment_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def delete_bulk_enrollment(self, enrollment_identities, api_key=None, expected_status_code=None):
        """
        Bulk enrollment delete
        :param enrollment_identities: Enrollment csv
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /device-enrollments-bulk-deletes response
        """
        api_url = '/{}/device-enrollments-bulk-deletes'.format(self.api_version)
        files = {'enrollment_identities': enrollment_identities}

        r = self.cloud_api.post(api_url, api_key, files=files, expected_status_code=expected_status_code)
        return r

    def get_certificate_enrollments(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get certificate enrollments
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /certificate-enrollments response
        """
        api_url = '/{}/certificate-enrollments'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_certificate_enrollment(self, certificate_enrollment_id, api_key=None, expected_status_code=None):
        """
        Get certificate enrollment
        :param certificate_enrollment_id: Certificate enrollment id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /certificate-enrollments/{enrollment_id} response
        """
        api_url = '/{}/certificate-enrollments/{}'.format(self.api_version, certificate_enrollment_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_certificate_renewal_request(self, device_id, certificate_name, api_key=None, expected_status_code=None):
        """
        Request certificate renewal
        :param device_id: Device id
        :param certificate_name: Certificate name
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /devices/{device-id}/certificates/{certificate-name}/renew response
        """
        api_url = '/{}/devices/{}/certificates/{}/renew'.format(self.api_version, device_id, certificate_name)

        r = self.cloud_api.post(api_url, api_key, expected_status_code=expected_status_code)
        return r
