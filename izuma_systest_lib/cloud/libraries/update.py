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
This module is for cloud's Update API functions
"""

from hashlib import md5
from base64 import b64encode


class UpdateAPI:
    """
    A class that provides Device management deployment related functionality.
    https://www.pelion.com/docs/device-management/current/service-api-references/update-service.html

    """

    def __init__(self, rest_api):
        """
        Initializes the Device Management Deployment library
        :param rest_api: RestAPI object
        """
        self.api_version = 'v3'
        self.cloud_api = rest_api

    def upload_firmware_image(self, firmware_binary_path, firmware_data=None, api_key=None, expected_status_code=None):
        """
        Upload firmware image
        :param firmware_binary_path: Path to firmware binary
        :param firmware_data: Firmware payload (optional)
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /firmware-images response
        """
        api_url = '/{}/firmware-images'.format(self.api_version)

        header_content = 'multipart/form-data'
        fw_image = {'datafile': open(firmware_binary_path, 'rb')}

        r = self.cloud_api.post(api_url, api_key, firmware_data, content_type=header_content, files=fw_image,
                                expected_status_code=expected_status_code)
        return r

    def get_firmware_image(self, image_id, api_key=None, expected_status_code=None):
        """
        Get firmware image
        :param image_id: Id for the image
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-image/{image_id} response
        """
        api_url = '/{}/firmware-images/{}'.format(self.api_version, image_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_firmware_images(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get firmware images
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-images response
        """
        api_url = '/{}/firmware-images'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_firmware_images_count(self, api_key=None, expected_status_code=None):
        """
        Get firmware images count
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: Firmware images count
        """
        api_url = '/{}/firmware-images'.format(self.api_version)
        query_params = {'limit': '5', 'include': 'total_count'}

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        images = r.json()
        return images['total_count']

    def delete_firmware_image(self, firmware_id, api_key=None, expected_status_code=None):
        """
        Delete firmware image
        :param firmware_id: Firmware id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /firmware-images/{firmware_id} response
        """
        api_url = '/{}/firmware-images/{}'.format(self.api_version, firmware_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_firmware_upload_job(self, upload_job_data, api_key=None, expected_status_code=None):
        """
        Create a new upload job
        :param upload_job_data: Upload job payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /firmware-images/upload-jobs response
        """
        api_url = '/{}/firmware-images/upload-jobs'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, upload_job_data, expected_status_code=expected_status_code)
        return r

    def get_firmware_upload_jobs(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get firmware upload jobs
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-images/upload-jobs response
        """
        api_url = '/{}/firmware-images/upload-jobs'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_firmware_upload_job(self, upload_job_id, api_key=None, expected_status_code=None):
        """
        Get firmware upload job
        :param upload_job_id: Upload job id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-images/upload-jobs/{upload_job_id} response
        """
        api_url = '/{}/firmware-images/upload-jobs/{}'.format(self.api_version, upload_job_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def update_firmware_upload_job(self, upload_job_id, upload_job_data, api_key=None, expected_status_code=None):
        """
        Update firmware upload job
        :param upload_job_id: Upload job id
        :param upload_job_data Upload job payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /firmware-images/upload-jobs/{upload_job_id} response
        """
        api_url = '/{}/firmware-images/upload-jobs/{}'.format(self.api_version, upload_job_id)

        r = self.cloud_api.put(api_url, api_key, upload_job_data, expected_status_code=expected_status_code)
        return r

    def delete_firmware_upload_job(self, upload_job_id, api_key=None, expected_status_code=None):
        """
        Delete firmware upload job
        :param upload_job_id: Upload job id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /firmware-images/upload-jobs/{upload_job_id} response
        """
        api_url = '/{}/firmware-images/upload-jobs/{}'.format(self.api_version, upload_job_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def append_chunks_firmware_upload_job(self, upload_job_id, api_key=None, expected_status_code=None):
        """
        Append a chunks to an upload job
        :param upload_job_id: Upload job id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /firmware-images/upload-jobs/{upload_job_id}/chunks response
        """
        api_url = '/{}/firmware-images/upload-jobs/{}/chunks'.format(self.api_version, upload_job_id)

        r = self.cloud_api.post(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_firmware_upload_job_all_chunks_metadata(self, upload_job_id, api_key=None, expected_status_code=None):
        """
        List all metadata for uploaded chunks
        :param upload_job_id: Upload job id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-images/upload-jobs/{upload_job_id}/chunks response
        """
        api_url = '/{}/firmware-images/upload-jobs/{}/chunks'.format(self.api_version, upload_job_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_firmware_upload_job_chunk_metadata(self, upload_job_id, chunk_id, api_key=None, expected_status_code=None):
        """
        Get metadata about a chunk
        :param upload_job_id: Upload job id
        :param chunk_id: Chunk id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-images/upload-jobs/{upload_job_id}/chunks/{chunk_id} response
        """
        api_url = '/{}/firmware-images/upload-jobs/{}/chunks/{}'.format(self.api_version, upload_job_id, chunk_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def upload_firmware_manifest(self, manifest_file_path, manifest_data=None, api_key=None, expected_status_code=None):
        """
        Upload firmware manifest
        :param manifest_file_path: Manifest file to post
        :param manifest_data: Manifest payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /firmware-manifests response
        """
        api_url = '/{}/firmware-manifests'.format(self.api_version)

        header_content = 'multipart/form-data'
        manifest_file = {'datafile': open(manifest_file_path, 'rb')}

        r = self.cloud_api.post(api_url, api_key, manifest_data, files=manifest_file, content_type=header_content,
                                expected_status_code=expected_status_code)
        return r

    def get_firmware_manifest(self, manifest_id, api_key=None, expected_status_code=None):
        """
        Get firmware manifest by id
        :param manifest_id: Id for the image
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-manifests/{manifest_id} response
        """
        api_url = '/{}/firmware-manifests/{}'.format(self.api_version, manifest_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_firmware_manifests(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get firmware manifests
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /firmware-manifests response
        """
        api_url = '/{}/firmware-manifests'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_firmware_manifests_count(self, api_key=None, expected_status_code=None):
        """
        Get firmware manifests count
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: Firmware manifests count
        """
        api_url = '/{}/firmware-manifests'.format(self.api_version)
        query_params = {'limit': '5', 'include': 'total_count'}

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        manifests = r.json()
        return manifests['total_count']

    def delete_firmware_manifest(self, manifest_id, api_key=None, expected_status_code=None):
        """
        Delete firmware manifest
        :param manifest_id: Manifest id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /firmware-manifests/{manifest_id} response
        """
        api_url = '/{}/firmware-manifests/{}'.format(self.api_version, manifest_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def create_update_campaign(self, campaign_data, api_key=None, expected_status_code=None):
        """
        Create update campaign
        :param campaign_data: Campaign payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /update-campaigns response
        """
        api_url = '/{}/update-campaigns'.format(self.api_version)

        r = self.cloud_api.post(api_url, api_key, campaign_data, expected_status_code=expected_status_code)
        return r

    def get_update_campaign(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Get a update campaign
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaign/{campaign_id} response
        """
        api_url = '/{}/update-campaigns/{}'.format(self.api_version, campaign_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def start_update_campaign(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Start update campaign
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /update-campaigns/{campaign_id}/start response
        """
        api_url = '/{}/update-campaigns/{}/start'.format(self.api_version, campaign_id)

        r = self.cloud_api.post(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def stop_update_campaign(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Stop update campaign
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: POST /update-campaigns/{campaign_id}/stop response
        """
        api_url = '/{}/update-campaigns/{}/stop'.format(self.api_version, campaign_id)

        r = self.cloud_api.post(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_update_campaign_metrics(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Get update campaign metrics
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaign/{campaign_id}/metrics response
        """
        api_url = '/{}/update-campaigns/{}/metrics'.format(self.api_version, campaign_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_update_campaign_statistics(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Get update campaign statistics
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaign/{campaign_id}/statistics response
        """
        api_url = '/{}/update-campaigns/{}/statistics'.format(self.api_version, campaign_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_update_campaign_summary_status(self, campaign_id, summary_status_id, api_key=None,
                                           expected_status_code=None):
        """
        Get update campaign summary status
        :param campaign_id: Campaign id
        :param summary_status_id: Summary status e.g fail
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaign/{campaign_id}/statistics/{summary_status_id} response
        """
        api_url = '/{}/update-campaigns/{}/statistics/{}'.format(self.api_version, campaign_id, summary_status_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_update_campaign_device_metadata(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Get update campaign device metadata
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaign/{campaign_id}/campaign-device-metadata response
        """
        api_url = '/{}/update-campaigns/{}/campaign-device-metadata'.format(self.api_version, campaign_id)

        r = self.cloud_api.get(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def get_update_campaigns(self, query_params=None, api_key=None, expected_status_code=None):
        """
        Get update campaigns
        :param query_params: e.g.{'limit': '1000', 'include': 'total_count'}
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaigns response
        """
        api_url = '/{}/update-campaigns'.format(self.api_version)

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        return r

    def get_update_campaigns_count(self, api_key=None, expected_status_code=None):
        """
        Get update campaigns count
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: GET /update-campaigns response
        """
        api_url = '/{}/update-campaigns'.format(self.api_version)
        query_params = {'limit': '5', 'include': 'total_count'}

        r = self.cloud_api.get(api_url, api_key, params=query_params, expected_status_code=expected_status_code)
        campaigns = r.json()
        return campaigns['total_count']

    def modify_update_campaign(self, campaign_id, campaign_data, api_key=None, expected_status_code=None):
        """
        Modify update campaign
        :param campaign_id: Campaign id
        :param campaign_data: Campaign payload
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: PUT /update-campaigns/{campaign_id} response
        """
        api_url = '/{}/update-campaigns/{}'.format(self.api_version, campaign_id)

        r = self.cloud_api.put(api_url, api_key, campaign_data, expected_status_code=expected_status_code)
        return r

    def delete_update_campaign(self, campaign_id, api_key=None, expected_status_code=None):
        """
        Delete update campaign
        :param campaign_id: Campaign id
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        :return: DELETE /update-campaigns/{campaign_id} response
        """
        api_url = '/{}/update-campaigns/{}'.format(self.api_version, campaign_id)

        r = self.cloud_api.delete(api_url, api_key, expected_status_code=expected_status_code)
        return r

    def upload_firmware_chunk(self, job_id, chunk, api_key=None, expected_status_code=None):
        """
        Upload chunk of firmware into cloud

        :param job_id: Upload job id
        :param chunk: Chunk of firmware to uplaod
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result in the function
        """
        api_url = '/{}/firmware-images/upload-jobs/{}/chunks'.format(self.api_version, job_id)
        headers = {'Content-MD5': b64encode(md5(chunk).digest()).decode('utf-8'),
                   'Content-type': 'binary/octet-stream',
                   'Content-Length': str(len(chunk))}

        r = self.cloud_api.post(api_url, api_key, payload=chunk, append_headers=headers, json_payload=False,
                                log_payload=False, expected_status_code=expected_status_code)
        return r
