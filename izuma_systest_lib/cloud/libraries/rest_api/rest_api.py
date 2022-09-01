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
This module is for RestAPI connection made with Requests library
"""

import inspect
import json
import logging
import time
from os import getenv
from urllib.parse import urlencode

import requests

from izuma_systest_lib.tools import assert_status, create_curl_command

log = logging.getLogger(__name__)

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.WARNING)

REST_TIMEOUT = int(getenv('REST_TIMEOUT', default='10'))


class RestAPI:
    """
    Rest API connection class - uses Requests library
    https://realpython.com/python-requests/

    """

    def __init__(self, rest_config_data, api_domain_key='api_gw'):
        """
        Initializes the RestAPI request class
        :param rest_config_data: Config data
        """
        config = rest_config_data

        self._log_commands = config.get('rest_log_commands', 'debug')
        self._log_command_body = config.get('rest_log_command_body', 'debug')
        self._log_responses = config.get('rest_log_responses', 'info')
        self._log_response_texts = config.get('rest_log_response_texts', 'debug')
        self._log_response_headers = config.get('rest_log_response_headers', 'debug')
        self._log_timing = config.get('rest_timing_logging', True)
        self._add_curl_logging = config.get('rest_add_curl_logging', 'debug')
        self._api_key_logging = config.get('rest_api_key_logging', False)
        self.api_gw = config[api_domain_key]
        self.api_key = config['api_key']
        self._client_certificate_and_key = None

        self.user_agent = config.get('rest_user_agent', 'SyTe FuTe')
        self.default_content_type = 'application/json'

        self.headers = {'User-Agent': '{}'.format(self.user_agent),
                        'Content-type': '{}'.format(self.default_content_type),
                        'Authorization': 'Bearer {}'.format(self.api_key)}

    @staticmethod
    def _log(level, msg):
        """
        Function making the actual logger logging
        :param level: Logger level
        :param msg: Content to be logged
        """
        if level == 'info':
            log.info(msg)
        elif level == 'debug':
            log.debug(msg)
        elif level == 'error':
            log.error(msg)
        elif level == 'warning':
            log.warning(msg)
        else:
            log.debug(msg)

    @staticmethod
    def _add_request_params(url, **kwargs):
        """
        Writes out the request params for logging purposes
        :param url: URL
        :param params: Request params
        :return: URL with request params
        """
        url_params = ''
        if 'params' in kwargs:
            params = kwargs.get('params')
            if isinstance(params, dict):
                url_params = '?{}'.format(urlencode(params))
            if isinstance(params, str):
                url_params = params
        return url + url_params

    @staticmethod
    def _data_content(headers, data):
        """
        Serializes payload data by the used content type
        :param headers: Request headers
        :param data: Payload data
        :return: Serialized payload data
        """
        if 'Content-type' in headers and data:
            if headers['Content-type'] == 'application/json':
                return json.dumps(data)
        return data

    @staticmethod
    def _clean_request_body(req_body):
        """
        Cleans the password from request body
        :param req_body: Request body
        :return: Cleaned body
        """
        if req_body is not None:
            if isinstance(req_body, str):
                split_body = req_body.split('&')
                for param in split_body:
                    if 'password=' in param:
                        pwd = param.split('=')[1]
                        req_body = req_body.replace('password={}'.format(pwd), 'password=*')
            if isinstance(req_body, bytes):
                req_body = 'body content in binary data - removed from the log'
        return req_body

    @staticmethod
    def _clean_response_text(resp):
        """
        Cleans the token from response
        :param resp: Request Response
        :return: Cleaned response
        """
        resp_text = resp.text
        try:
            resp_dict = resp.json()
            if resp_dict.get('token') is not None:
                resp_dict['token'] = '*'
                resp_text = str(resp_dict)
        except (AttributeError, json.JSONDecodeError):
            pass
        return resp_text

    def _write_log_response(self, method, api_url, r, measured_time):
        """
        Function handling the response logging
        :param method: GET, PUT, POST, etc to be written in short response log
        :param api_url: API endpoint url where the response came from
        :param r: The response itself
        :param measured_time: Time spent on rest request
        """
        if self._log_command_body != 'none':
            req_body = self._clean_request_body(r.request.body)
            self._log(self._log_command_body, 'Request body: {}'.format(req_body))
        if self._log_responses != 'none':
            self._log(self._log_responses, '{} {} - Response: {} - X-Request-ID: {}'.
                      format(method, api_url, r.status_code, r.headers.get('X-Request-ID', '')))
        if self._log_timing:
            log.debug('{} {} - [time][{:.4f} s]'.format(method, api_url, measured_time))
        if self._log_response_texts != 'none':
            resp_text = self._clean_response_text(r)
            self._log(self._log_response_texts, 'Response text: {}'.format(resp_text))
        if self._log_response_headers != 'none':
            self._log(self._log_response_headers, 'Response headers: {}'.format(r.headers))

    def _do_request(self, method, api_url, request_headers=None, certificate=None, request_data=None, files=None,
                    timeout=REST_TIMEOUT, logged_payload=None, expected_status_code=None, **kwargs):
        """
        Function making the actual rest request
        :param method: Request method 'get/put/post/etc'
        :param api_url: API url
        :param request_headers: Request headers
        :param timeout: Request timeout
        :param certificate: Certificate
        :param request_data: Request payload data
        :param files: Files to send
        :param expected_status_code: Expected response status code
        :param kwargs: Other arguments used in the requests. http://docs.python-requests.org/en/master/api/
        :return: Request response
        """
        log.debug(request_headers)
        log_head = request_headers.copy()
        if self._log_commands != 'none':
            if not self._api_key_logging:
                log_head['Authorization'] = 'Bearer API_KEY'
            if not logged_payload:
                logged_payload = request_data
            self._log(self._log_commands,
                      '{}: {}  Headers: {}  Payload: {}'.format(method.upper(), self._add_request_params(api_url,
                                                                                                         **kwargs),
                                                                log_head, logged_payload))
        if self._add_curl_logging != 'none':
            self._log(self._add_curl_logging, create_curl_command(log_head['Authorization'], None, method,
                                                                  self._add_request_params(api_url, **kwargs), '-v',
                                                                  self._api_key_logging))
        if not certificate:
            certificate = self._client_certificate_and_key

        try:
            time_start = time.time()

            r = requests.request(method.upper(), api_url, headers=request_headers, cert=certificate,
                                 data=request_data, files=files, timeout=timeout, **kwargs)

            time_end = time.time()

            self._write_log_response(method.upper(), api_url, r, time_end - time_start)
            if expected_status_code is not None:
                assert_status(r, inspect.stack()[1][3].upper(), expected_status_code, api_url)
            return r

        except requests.exceptions.RequestException as e:
            log.error('Requests library raised exception for call {} {} - '
                      'expected status code: {} - exception message: {}'.format(method.upper(), api_url,
                                                                                expected_status_code, e))
            raise

    def use_client_certificate(self, certificate_filename, private_key_filename):
        """
        Set client certificate to use with requests
        :param certificate_filename: Certificate file name
        :param private_key_filename: Private key file name
        """
        # Make sure api key isn't used for auth in requests
        # Using a client certificate disables api key auth
        self.api_key = None
        del self.headers['Authorization']

        self._client_certificate_and_key = (certificate_filename, private_key_filename)

    def login(self, account, username, password, expected_status_code=None):
        """
        User login
        :param account: Account id
        :param username: User id
        :param password: Password
        :param expected_status_code: Asserts the result's status code
        :return: Login response
        """
        log.info('Logging in user "{}" to account "{}"'.format(username, account))
        api_url = '/auth/login'
        url = '{}{}'.format(self.api_gw, api_url)
        payload = {'username': username, 'password': password, 'account': account}

        time_start = time.time()
        r = requests.post(url, data=payload, timeout=REST_TIMEOUT)
        time_end = time.time()

        self._write_log_response('Login', api_url, r, time_end - time_start)
        if expected_status_code is not None:
            assert_status(r, inspect.stack()[1][3], expected_status_code, api_url)

        return r

    def logout(self, rt_token=None, expected_status_code=None):
        """
        User logout
        :return: Logout response
        """
        headers = self.headers
        if rt_token is not None:
            headers['Authorization'] = rt_token
        api_url = '/auth/logout'
        url = '{}{}'.format(self.api_gw, api_url)

        time_start = time.time()
        r = requests.post(url, headers=headers, timeout=REST_TIMEOUT)
        time_end = time.time()

        self._write_log_response('Logout', api_url, r, time_end - time_start)
        if expected_status_code is not None:
            assert_status(r, inspect.stack()[1][3], expected_status_code, api_url)

        return r

    def get(self, api_url, api_key=None, expected_status_code=None, **kwargs):
        """
        GET
        :param api_url: API URL
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result's status code
        :param kwargs: Other arguments used in the requests. http://docs.python-requests.org/en/master/api/
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        return self._do_request('get', url, request_headers, expected_status_code=expected_status_code, **kwargs)

    def put(self, api_url, api_key=None, payload=None, content_type=None, expected_status_code=None, **kwargs):
        """
        PUT
        :param api_url: API URL
        :param api_key: Authentication key
        :param payload: PUT request payload
        :param content_type: Message content-type
        :param expected_status_code: Asserts the result's status code
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        if content_type:
            request_headers['Content-type'] = content_type
        else:
            request_headers['Content-type'] = self.default_content_type

        request_data = self._data_content(request_headers, payload)

        return self._do_request('put', url, request_headers, request_data=request_data,
                                expected_status_code=expected_status_code, **kwargs)

    def post(self, api_url, api_key=None, payload=None, content_type=None, files=None, json_payload=True,
             append_headers=None, log_payload=True, expected_status_code=None, **kwargs):
        """
        POST
        :param api_url: API URL
        :param api_key: Authentication key
        :param json_payload: Set True if payload is json formatted data.
        :param content_type: Message content-type
        :param files: Files to post
        :param payload: POST request payload
        :param append_headers: Add headers
        :param log_payload: Set false to hide big payloads from being logged
        :param expected_status_code: Asserts the result's status code
        :param kwargs: Other arguments used in the requests. http://docs.python-requests.org/en/master/api/
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        if content_type:
            request_headers['Content-type'] = content_type
        else:
            request_headers['Content-type'] = self.default_content_type

        # Add custom headers
        if append_headers is not None:
            request_headers.update(append_headers)

        # This is our cloud's bug IOTUPD-3685 - when sending files with requests library, leave the content-type out
        if files is not None:
            request_headers.pop('Content-type')

        if log_payload:
            logged_payload = payload
        else:
            logged_payload = 'log_payload set to False'

        if payload:
            if json_payload:
                payload = json.dumps(payload)

        return self._do_request('post', url, request_headers, request_data=payload, files=files,
                                logged_payload=logged_payload, expected_status_code=expected_status_code, **kwargs)

    def delete(self, api_url, api_key=None, payload=None, expected_status_code=None):
        """
        DELETE
        :param api_url: API URL
        :param api_key: Authentication key
        :param payload: DELETE request payload
        :param expected_status_code: Asserts the result's status code
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        request_data = self._data_content(request_headers, payload)

        return self._do_request('delete', url, request_headers, request_data=request_data,
                                expected_status_code=expected_status_code)

    def patch(self, api_url, api_key=None, payload=None, content_type=None, expected_status_code=None):
        """
        PATCH
        :param api_url: API URL
        :param api_key: Authentication key
        :param payload: PATCH request payload
        :param content_type: Message content-type
        :param expected_status_code: Asserts the result's status code
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        if content_type:
            request_headers['Content-type'] = content_type
        else:
            request_headers['Content-type'] = self.default_content_type

        request_data = self._data_content(request_headers, payload)

        return self._do_request('patch', url, request_headers, request_data=request_data,
                                expected_status_code=expected_status_code)

    def head(self, api_url, api_key=None, expected_status_code=None, **kwargs):
        """
        HEAD
        :param api_url: API URL
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result's status code
        :param kwargs: Other arguments used in the requests. http://docs.python-requests.org/en/master/api/
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        return self._do_request('head', url, request_headers, expected_status_code=expected_status_code, **kwargs)

    def options(self, api_url, api_key=None, expected_status_code=None, **kwargs):
        """
        OPTIONS
        :param api_url: API URL
        :param api_key: Authentication key
        :param expected_status_code: Asserts the result's status code
        :param kwargs: Other arguments used in the requests. http://docs.python-requests.org/en/master/api/
        :return: Request response
        """
        request_headers = self.headers
        url = '{}{}'.format(self.api_gw, api_url)

        if api_key:
            key = api_key
        else:
            key = self.api_key
        if key:
            request_headers['Authorization'] = 'Bearer {}'.format(key)

        return self._do_request('options', url, request_headers, expected_status_code=expected_status_code, **kwargs)
