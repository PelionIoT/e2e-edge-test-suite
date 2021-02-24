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

import logging

log = logging.getLogger(__name__)


class TemporaryAccessKey:
    def __init__(self, cloud_api, application_id, access_key=None):
        log.info('Creating new temporary access key')
        self.cloud_api = cloud_api
        self.application_id = application_id
        self.access_key_ret = self.cloud_api.iam.create_access_key(self.application_id, access_key=access_key,
                                                                   expected_status_code=201).json()

    @property
    def key_id(self):
        return self.access_key_ret['id']

    @property
    def key(self):
        return self.access_key_ret['key']

    def delete(self):
        log.info('Cleaning out the generated access key, id: {}'.format(self.key_id))
        self.cloud_api.iam.delete_access_key(self.application_id, self.key_id, expected_status_code=204)
