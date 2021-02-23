# pylint: disable=bare-except
"""
General utility functions for library and test cases
"""

import functools

import inspect
import json
import logging
import os
import random
import re

import string
import subprocess
import time
from time import sleep
from uuid import uuid4

log = logging.getLogger(__name__)

ANSI_ENG = re.compile(r'\033\[((?:\d|;)*)([a-zA-Z])'.encode())


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
    :return: Comparision result
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


def build_random_string(str_length, use_digits=False, use_punctuations=False):
    r"""
    Create random string
    :param str_length: String length
    :param use_digits: Takes string.digits as well
    :param use_punctuations: Takes string.punctuation without "\, ", '"
    :return: Random string
    """
    letters = string.ascii_letters
    if use_digits:
        letters = letters + string.digits
    if use_punctuations:
        letters = letters + string.punctuation.replace(" ", "").replace("\\", "").replace("\"", "").replace("\'", "")
    return ''.join(random.choice(letters) for _ in range(str_length))


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


def create_psk(use_uuid=True, epn_length=32, use_punctuations=False, secret_length=32,
               letter_case='lower', secret_prefix=None):
    """
    Create a unique PSK
    :use_uuid: Use uuid to create a PSK
    :epn_length: endpoint_name length as ASCII characters
    :use_punctuations: Use punctuation characters in endpoint_name
    :secret_length: secret_hex length as hex digits
    :letter_case: Use upper/lower/mixed case letters in secret_hex
    :secret_prefix: secret_hex prefix as string
    :returns: A dictionary {"endpoint_name": <ascii string>, "secret_hex": <hex string>}
    """
    if use_uuid:
        psk = {
            'endpoint_name': uuid4().hex,
            'secret_hex': uuid4().hex
        }
    else:
        endpoint_name = build_random_string(epn_length, use_punctuations=use_punctuations)
        secret_as_hex = build_random_string(secret_length, use_punctuations=use_punctuations)

        if letter_case == 'lower':
            secret_as_hex = secret_as_hex.lower()
        elif letter_case == 'upper':
            secret_as_hex = secret_as_hex.upper()
        else:
            pass
        if secret_prefix is not None:
            secret_as_hex = secret_prefix + secret_as_hex
        psk = {
            'endpoint_name': endpoint_name,
            'secret_hex': secret_as_hex
        }
    return psk


def ascii_str_to_c_hex_byte_array(ascii_string):
    """
    Convert an ASCII string to a C hex byte array
    :string: A string
    :returns: C hex byte array as a string
    """
    hex_byte_array = ''
    for char in ascii_string:
        hex_byte_array = hex_byte_array + hex(ord(char)) + ', '
    # delete last ", "
    hex_byte_array = hex_byte_array[:-2]
    return hex_byte_array


def hex_str_to_c_hex_byte_array(hex_string):
    """
    Convert an hex string to a C hex byte array
    :string: A hex string
    :returns: C hex byte array as a string
    """
    hex_byte_array = ''
    bytearr = bytearray.fromhex(hex_string)
    for byte in bytearr:
        hex_byte_array = hex_byte_array + hex(byte) + ', '
    # delete last ", "
    hex_byte_array = hex_byte_array[:-2]
    return hex_byte_array


def strip_escape(string_to_escape):
    """
    Strip escape characters from string.
    :param string_to_escape: string to work on
    :return: stripped string
    """

    matches = []
    for match in ANSI_ENG.finditer(string_to_escape):
        matches.append(match)
    matches.reverse()
    for match in matches:
        start = match.start()
        end = match.end()
        string_to_escape = string_to_escape[0:start] + string_to_escape[end:]
    return string_to_escape


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


def get_from_json(file, key):
    """
    Find and return value of a key in a JSON

    :param file: JSON file
    :param key: Key in JSON
    :return: Value of a key. None if key is not found
    """
    with open(file) as json_file:
        data = json.load(json_file)
    try:
        value = data[key]
        return value
    except KeyError:
        log.debug('{} not found in {}'.format(key, os.path.basename(file)))
        return None


def set_to_json(file, key, value):
    """
    Set key & value pair to a JSON

    :param file: JSON file
    :param key: Key in JSON
    :param value: Value of the key
    """
    with open(file, "r") as json_file:
        data = json.load(json_file)
    data[key] = value
    with open(file, "w") as json_file:
        json.dump(obj=data, fp=json_file, indent=4)


def delete_in_json(file, key):
    """
    Delete a key in a JSON

    :param file: JSON file
    :param key: Key in JSON
    """
    with open(file, "r") as json_file:
        data = json.load(json_file)
    del data[key]
    with open(file, "w") as json_file:
        json.dump(obj=data, fp=json_file, indent=4)


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
        except:
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
