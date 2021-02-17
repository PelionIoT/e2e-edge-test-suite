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
    or api key and api url given via env variables,
    or creates temp account if started with root admin login
    :param request: Request object
    :return: Cloud API object
    """
    log.debug('Initializing Cloud API fixture')

    temp_account_id = None
    tc_conf = {}

    # If user doesn't give json config path, let's initialize cloud with given root login
    # or api key and url defined in env variables
    if not request.config.getoption('config_path'):
        # Setting the api key logging to config
        if request.config.getoption('show_api_key'):
            tc_conf['rest_api_key_logging'] = (request.config.getoption('show_api_key') == 'true')

        # If root login and url are given on start up arguments, let's create temp account for tests
        if request.config.getoption('api_gw') and request.config.getoption('rt_user') and \
                request.config.getoption('rt_password'):

            log.debug('Creating temporary account and api key')
            # Fill the root info and initialize cloud
            tc_conf['api_gw'] = request.config.getoption('api_gw')
            tc_conf['api_key'] = ''
            tc_conf['root_user_id'] = request.config.getoption('rt_user')
            tc_conf['root_password'] = request.config.getoption('rt_password')

            pelion_cloud = PelionCloud(tc_conf)
            r = pelion_cloud.rest_api.login('', request.config.getoption('rt_user'),
                                            request.config.getoption('rt_password'))
            assert r.status_code == 200, 'Failed to login root user!'
            resp = r.json()
            log.info('Root admin logged in')

            # Create temp account for tests and fill its info to test configs
            r = pelion_cloud.iam.create_account(api_key=resp['token'])
            assert r.status_code == 201, 'Failed to create account!'
            resp = r.json()
            log.info('Temporary account created for tests, account id: {}'.format(resp['id']))

            tc_conf['api_key'] = resp['admin_key']
            tc_conf['account_id'] = resp['id']
            tc_conf['account'] = resp['aliases'][0]
            tc_conf['user_id'] = resp['email']
            tc_conf['password'] = resp['admin_password']

            temp_account_id = resp['id']

        # If user doesn't give json config path nor root login, there's option to initialize cloud via two env variables
        elif os.environ.get('PELION_CLOUD_API_KEY') and os.environ.get('PELION_CLOUD_API_URL'):
            log.info('Using api key and api url defined in environment variables')
            tc_conf['api_gw'] = os.environ.get('PELION_CLOUD_API_URL')
            tc_conf['api_key'] = os.environ.get('PELION_CLOUD_API_KEY')
            tc_conf['root_user_id'] = ''
            tc_conf['root_password'] = ''

        else:
            error_msg = 'Give config json or api url and root login in start up arguments, or set env variables for ' \
                        'api key (PELION_CLOUD_API_KEY) and api url (PELION_CLOUD_API_URL).'
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

    log.debug('Cleaning out the Cloud API fixture')
    if temp_account_id is not None:
        log.info('Deleting temporary account, id: {}'.format(temp_account_id))
        r = pelion_cloud.rest_api.login('', request.config.getoption('rt_user'),
                                        request.config.getoption('rt_password'))
        resp = r.json()

        r = pelion_cloud.iam.delete_account(temp_account_id, api_key=resp['token'])
        assert r.status_code == 204, 'Failed to delete temporary test account! Id: {}'.format(temp_account_id)


@pytest.fixture(scope='module')
def global_data():
    """
    Fixture for using global data (variables) inside test module.
    If you need global data variable, add it to Data class
    :return: Data class to be used inside module
    """

    class Data:
        def __init__(self):
            self.billing_wait = True

    return Data()


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
