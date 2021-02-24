# pylint: disable=redefined-outer-name
"""
General pytest fixtures
"""

import logging
import os
import pytest
import pelion_systest_lib.tools as utils

from pelion_systest_lib.cloud.cloud import PelionCloud
from pelion_systest_lib.cloud.libraries.rest_api.rest_api import RestAPI

log = logging.getLogger(__name__)

pytest.global_test_env_config = {}


@pytest.fixture(scope='session')
def tc_config_data(request):
    """
    Fixture for accessing test case config json given with '--config_path' argument
    :param request: Request object
    :return: Config data object
    """
    if request.config.getoption('config_path'):
        log.debug('Getting test configs from json')
        return utils.load_config(request.config.getoption('config_path'))
    if pytest.global_test_env_config != {}:
        log.debug('Getting test configs from global variable')
        return pytest.global_test_env_config
    raise AssertionError('Test configuration is not defined. Use --config_path=<path to define config file>')


@pytest.fixture(scope='session')
def cloud_api(request):
    """
    Fixture for cloud API
    Initializes the rest api with the api key given in test case config
    :param request: Request object
    :return: Cloud API object
    """
    log.debug('Initializing Cloud API fixture')

    tc_conf = {}

    # If user doesn't give json config path, let's initialize cloud with given root login
    # or api key and url defined in env variables
    if not request.config.getoption('config_path'):
        # Setting the api key logging to config
        if request.config.getoption('show_api_key'):
            tc_conf['rest_api_key_logging'] = (request.config.getoption('show_api_key') == 'true')

        else:
            error_msg = 'Connfiguration error in config json'
            log.error(error_msg)
            assert False, error_msg

        # Initialize cloud either with temp account info or info from env variables
        pytest.global_test_env_config = tc_conf
        pelion_cloud = PelionCloud(tc_conf)

    else:
        log.info('Using account and api key defined in config json {}'.format(request.config.getoption('config_path')))
        tc_conf = utils.load_config(request.config.getoption('config_path'))
        pytest.global_test_env_config = tc_conf
        pelion_cloud = PelionCloud(tc_conf)

    log.info('Cloud API object initialized for {} and account id {}'.format(tc_conf.get('api_gw', ''),
                                                                            tc_conf.get('account_id', '')))

    yield pelion_cloud


@pytest.fixture(scope='function')
def rest_api():
    """
    Fixture for initializing only the rest API request layer - usable for API testing
    Initialize the URL and authentication token by the environment variables
    :return: Rest API class
    """
    config = {'api_gw': os.environ.get('REST_API_URL'),
              'api_key': os.environ.get('REST_API_TOKEN'),
              'rest_user_agent': os.environ.get('REST_API_USER_AGENT', 'SystemTesting')}

    return RestAPI(config)
