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
General utility functions for library and test cases
"""

import functools

import inspect
import json
import logging
import os
import re
import subprocess
import time
import string
import random
from time import sleep

log = logging.getLogger(__name__)


def load_config(config_path):
    """
    Load JSON config file defined at function parameter
    :param config_path: Config json file path
    :return: Test config object
    """
    config_data = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as config_file:
                config_data = json.load(config_file)

        except ValueError as e:
            error_msg = 'JSON syntax error on test configs from path: {}, {}'.format(config_path, e)
            log.error(error_msg)
            raise AssertionError(error_msg)

    return config_data


def build_random_string(str_length, use_digits=False, use_punctuations=False):
    """
    Create random string
    :param str_length: String length
    :param use_digits: Takes string.digits as well
    :param use_punctuations: Takes string.punctuation
    :return: Random string
    """
    letters = string.ascii_letters
    if use_digits:
        letters = letters + string.digits
    if use_punctuations:
        letters = letters + string.punctuation.replace(" ", "").replace("\\", "").replace("\"", "").replace("\'", "")
    return ''.join(random.choice(letters) for _ in range(str_length))


def assert_status(response, func, expected_resp, api_url=''):
    """
    Function for asserting response and creating proper msg on fail situation
    :param response: Rest API response
    :param func: Calling function
    :param expected_resp: Expected response or list of expected responses
    :param api_url: Called rest API url
    """
    if _assert_status(expected_resp, response) is False:
        error_msg = 'ERROR: "{}" {} failed!\n' \
                    'Expected result {} -> actual response was: {}\n\n' \
                    'Response body: {}\n' \
                    'Response headers: {}'.format(func,
                                                  api_url,
                                                  expected_resp,
                                                  response.status_code,
                                                  response.text,
                                                  response.headers)
        log.error(error_msg)
        assert False, error_msg


def _assert_status(expected_resp, response):
    """
    Status code comparison
    :param expected_resp: Expected response, one value or list of values
    :param response: Request response
    :return: Comparison result
    """
    if isinstance(expected_resp, list):
        return response.status_code in expected_resp
    return response.status_code == expected_resp


def create_curl_command(authorization, payload, command, url, curl_options, show_api_key,
                        content_type='application/json'):
    """
    cURL command generator
    :param authorization: Authorization part e.g Bearer API key
    :param payload: Payload data
    :param command: GET, PUT, etc
    :param url: API url
    :param curl_options: E.g. '-v' for verbose
    :param show_api_key: Showing actual api-key or not
    :param content_type: Content type
    :return: cURL command string
    """
    if show_api_key is False:
        authorization = 'Bearer API_KEY'

    headers = '-H \'Authorization: {}\' -H \'Content-type: {}\''.format(authorization, content_type)

    if payload is not None:
        cc = 'curl {} -d \'{}\' -X {} \'{}\' {}'.format(headers, payload, command.upper(), url, curl_options)
    else:
        cc = 'curl {} -X {} \'{}\' {}'.format(headers, command.upper(), url, curl_options)

    return cc


def retry(func, *args, retry_condition, retry_count=3, delay=5, **kwargs):
    """
    Set retry around the function call to retry if response is not the wanted one
    Usage:
    retry(function_to_retry, func_param_1, func_param_2, retry_condition={'response_contains': 'find this'},
                                                                                    retry_count=3, delay=1))

    :param func: Function to retry
    :param retry_condition: Dictionary for conditions,
                            supported keys: rest_response_code|response_length|response_contains
    :param retry_count: Retry amount
    :param delay: Delay in seconds between retry
    :return: Function response after conditions match or finally what ever is returning
    """
    resp = None
    for i in range(1, retry_count + 1):
        resp = func(*args, **kwargs)
        if retry_condition is not None:
            if 'rest_response_code' in retry_condition and \
                    _check_retry_condition(resp.status_code, retry_condition['rest_response_code'], func.__name__, i,
                                           retry_count):
                break
            if 'response_length' in retry_condition and \
                    _check_retry_condition(len(resp), retry_condition['response_length'], func.__name__, i,
                                           retry_count):
                break
            if 'response_contains' in retry_condition and \
                    _check_retry_condition(True, retry_condition['response_contains'] in resp, func.__name__, i,
                                           retry_count, haystack=resp, needle=retry_condition['response_contains']):
                break
            log.debug('No supported implementation for retry clause "{}"'.format(retry_condition))
            break
        sleep(delay)
    return resp


def _check_retry_condition(clause, condition, name, attempt, retry_count, haystack=None, needle=None):
    """
    Checking the actual retry condition
    :param clause: Clause
    :param condition: Condition
    :param name: Function name
    :param attempt: Attempt count
    :param retry_count: Retry count
    :param haystack: Haystack
    :param needle: Needle
    :return: True/False
    """
    if condition == clause:
        return True
    if not haystack:
        log.debug('Retry {}/{} for function {} - Returned "{}" not matching to expected one "{}"'.format(
            attempt, retry_count, name, condition, clause))
    else:
        log.debug('Retry {}/{} for function {} - Returned "{}" not containing "{}"'.format(
            attempt, retry_count, name, haystack, needle))
    return False


def retry_decorator(retry_condition, retry_count=3, delay=5):
    """
    Set retry decorator over the function that needs to be retried again if response is not the wanted one
    Decorator usage:
    @retry_decorator({'response_length': 15}, 3, 1)
    def function_to_retry():

    :param retry_condition: Dictionary for conditions,
                            supported keys: rest_response_code|response_length|response_contains
    :param retry_count: Retry amount
    :param delay: Delay in seconds between retry
    :return: Function response after conditions match or finally what ever is returning
    """

    def retry_deco(func):
        @functools.wraps(func)
        def retry_wrapper(*args, **kwargs):
            return retry(func, *args, retry_condition=retry_condition, retry_count=retry_count, delay=delay, **kwargs)

        return retry_wrapper

    return retry_deco


def deprecated(msg):
    """
    Deprecated decorator for obsolete function before cleaning them out from the library
    :param msg: Note from the decorator's side - e.g. "use [this function] instead"
    :return:
    """

    def deprecated_deco(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            if inspect.isclass(func):
                target = 'class'
            else:
                target = 'function'
            log.warning('Call to deprecated {} [{}] - "{}"'.format(target, func.__name__, msg))
            return func(*args, **kwargs)

        return new_func

    return deprecated_deco


def sanitize(text):
    """ Sanitizing output text:
    - Replazing apikey with four stars
    """
    return re.sub(r'ak_[a-zA-Z0-9]+', '****', text)


def execute_local_command(command, assert_error=True):
    """ General function for most of local execution needs """
    log.info('Executing local command: {}'.format(command))
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stdout:
        stdout = stdout.decode(errors='ignore')
        log.info('stdout {}'.format(sanitize(stdout)))
    if stderr:
        stderr = stderr.decode(errors='ignore')
        log.info('stderr {}'.format(sanitize(stderr)))
        if assert_error and 'error' in stderr.lower():
            raise Exception('Error happened during command "{}"execution!'.format(command))
    if not stdout and stderr:
        return stderr
    return stdout if stdout else ''


def execute_with_retry(command, assert_text, timeout=10 * 60, delay_in_sec=5, assert_response=False):
    start_time = time.time()
    i = 0
    while True:
        try:
            response = execute_local_command(command)
        except Exception as err:
            log.warning('Command execution error: {}'.format(err))
            response = ''

        if assert_text in response:
            return response

        if time.time() - start_time > timeout:
            if assert_response:
                raise Exception("Timeout: The thing did not happen in {} seconds".format(timeout))
            return ''

        time.sleep(delay_in_sec)
        i = i + 1
        log.info('{}. retry: {}'.format(i, command))


def build_random_enrollment_identity():
    """
    Create random identity for enrollment
    :return: Identity string
    """
    identity = 'A-35'
    for _ in range(31):
        identity += ':'
        identity += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(2))

    return identity
