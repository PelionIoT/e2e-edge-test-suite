# pylint: disable=redefined-outer-name
"""
Edge related pytest fixtures
"""

import logging
import os
import tempfile

import pytest
from kubernetes.client import Configuration
from kubernetes.config import load_kube_config

import pelion_systest_lib.tools as utils
from pelion_systest_lib.cloud.cloud import PelionCloud
from pelion_systest_lib.cloud.edge_cloud import PelionEdgeCloud
from pelion_systest_lib.edge.connection.connector import EdgeConnector
from pelion_systest_lib.edge.kaas import Kaas
from pelion_systest_lib.edge.kubectl import Kubectl

log = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def edge_gateway_developer_certificate(cloud_api, tc_config_data):
    """
    Ensures device certificate and private key exist in temporary files and
    that those paths exist in the tc_config
    :param cloud_api: PelionCloud instance
    :param tc_config_data: Default test config
    :return: A tuple: (certificate_id, certificate_file_name, private_key_file_name)
    """
    temp_cert_id = None

    if 'edge_cert_file' in tc_config_data and 'edge_key_file' in tc_config_data and 'edge_cert_id' in tc_config_data:
        log.debug('Using edge certificate, edge key, and edge certificate CN defined in config json')
        certificate_file_name = tc_config_data['edge_cert_file']
        certificate_key_file_name = tc_config_data['edge_key_file']
        certificate_id = tc_config_data['edge_cert_id']
    else:
        log.info('Creating new developer certificate for test module')
        payload = {'name': 'edge-pytest-{}'.format(utils.build_random_string(8, True)),
                   'description': 'developer certificate for testing'}
        response = cloud_api.iam.create_developer_certificate(payload, expected_status_code=201).json()

        log.info('Created new developer certificate for test module, id: {}'.format(response['id']))

        certificate_fd = tempfile.NamedTemporaryFile()
        private_key_fd = tempfile.NamedTemporaryFile()
        certificate_fd.write(bytes(response['developer_certificate'], 'utf8'))
        private_key_fd.write(bytes(response['developer_private_key'], 'utf8'))
        certificate_file_name = certificate_fd.name
        certificate_key_file_name = private_key_fd.name
        temp_cert_id = response['id']
        certificate_id = temp_cert_id
        certificate_fd.flush()
        private_key_fd.flush()

    yield certificate_id, certificate_file_name, certificate_key_file_name

    if temp_cert_id is not None:
        log.info('Deleting temporary developer certificate files: {} and {}'.format(certificate_file_name,
                                                                                    certificate_key_file_name))
        certificate_fd.close()
        private_key_fd.close()
        log.info('Cleaning out the generated test module developer api key, id: {}'.format(response['id']))
        r = cloud_api.iam.delete_trusted_certificate(response['id'], expected_status_code=204)
        assert r.status_code == 204, 'Failed to delete temporary developer certificate! Id: {}'.format(temp_cert_id)


@pytest.fixture(scope='module')
def tc_config_data_with_edge(request, tc_config_data):
    """
    Ensures edge-k8s and gateways domain are part of the tc_config_data object
    :param request: Request object
    :param tc_config_data: Default test config
    :return: Config data object
    """
    if 'edge_k8s_url' not in tc_config_data:
        if request.config.getoption('edge_k8s_url'):
            tc_config_data['edge_k8s_url'] = request.config.getoption('edge_k8s_url')
        elif os.environ.get('PELION_CLOUD_EDGE_K8S_URL'):
            log.info('Using edge-k8s api url defined in environment variable')
            tc_config_data['edge_k8s_url'] = os.environ.get('PELION_CLOUD_EDGE_K8S_URL')
        else:
            error_msg = 'Give config json or edge-k8s api url in start up arguments, or set env variables for ' \
                        'edge-k8s api url (PELION_CLOUD_EDGE_K8S_URL).'
            log.error(error_msg)
            assert False, error_msg
    if 'gateways_url' not in tc_config_data:
        if request.config.getoption('gateways_url'):
            tc_config_data['gateways_url'] = request.config.getoption('gateways_url')
        elif os.environ.get('PELION_CLOUD_GATEWAYS_URL'):
            log.info('Using edge-k8s api url defined in environment variable')
            tc_config_data['gateways_url'] = os.environ.get('PELION_CLOUD_GATEWAYS_URL')
        else:
            error_msg = 'Give config json or gateways api url in start up arguments, or set env variables for ' \
                        'gateways api url (PELION_CLOUD_GATEWAYS_URL).'
            log.error(error_msg)
            assert False, error_msg

    return tc_config_data


@pytest.fixture(scope='function')
def cloud_api_with_edge(tc_config_data_with_edge):
    """
    Generates a PelionCloud object with active rest_api_gateways
    and rest_api_edge_k8s clients. Both clients use API key for
    auth
    :param tc_config_data_with_edge: Modified test config
    :return: PelionCloud object
    """
    return PelionCloud(tc_config_data_with_edge)


@pytest.fixture(scope='function')
def cloud_api_with_edge_certs(tc_config_data_with_edge):
    """
    Generates a PelionCloud object with active rest_api_gateways
    and rest_api_edge_k8s clients. Both clients use client certificate
    for auth
    :param tc_config_data_with_edge: Modified test config
    :return: PelionCloud object
    """
    pelion_cloud = PelionCloud(tc_config_data_with_edge)
    pelion_cloud.rest_api_gateways.use_client_certificate(tc_config_data_with_edge['edge_cert_file'],
                                                          tc_config_data_with_edge['edge_key_file'])
    pelion_cloud.rest_api_edge_k8s.use_client_certificate(tc_config_data_with_edge['edge_cert_file'],
                                                          tc_config_data_with_edge['edge_key_file'])

    return pelion_cloud


@pytest.fixture(scope='session')
def kube_config_file_path(tc_config_data):
    """
    Create temporary configuration file
    :param tc_config_data:
    :return:
    """
    kube_config_path = tc_config_data.get('kubernetes_configuration_file', '')
    is_temporary = False

    # If kube configuration file is missing, add it to the disk
    if 'edge_k8s_url' in tc_config_data \
            and 'api_key' in tc_config_data \
            and not kube_config_path:
        log.debug('Creating kubernetes configuration file')
        kube_config_path = Kubectl().write_kubectl_config(
            server_url=tc_config_data['edge_k8s_url'],
            api_key=tc_config_data['api_key'])
        if not os.environ.get('JENKINS_URL', False):
            is_temporary = True

        # Set kubectl to use new configuration file
        os.environ['KUBECONFIG'] = kube_config_path
        log.debug('KUBECONFIG={}'.format(os.environ['KUBECONFIG']))

        # Take configuration in use
        utils.execute_local_command('kubectl config use-context edge-k8s')
        log.debug('Temporary kubernetes configuration successfully created and in use')
    else:
        log.debug('No need to create temporary kubernetes konfiguration')
    yield kube_config_path

    # Remove temporary configuration when running outside Jenkins
    if is_temporary:
        log.debug('Removing temporary kube config: {}'.format(kube_config_path))
        os.remove(kube_config_path)


@pytest.fixture(scope='session')
def edge(kube_config_file_path, tc_config_data):
    """
    Initializes connection to edge via RaaS or locally (subprocess) based on configuration.
    Release connection when not needed anymore
    :param kube_config_file_path: Kubernetes konfiguration file path
    :param tc_config_data: Test case config
    :return: resource
    """
    edge = EdgeConnector(tc_config_data)
    try:
        edge.connect_edge()
    except BaseException as e:
        if not tc_config_data.get('edge_skip_release_if_setup_error', False):
            edge.release()
        raise e

    yield edge

    edge.release()







@pytest.fixture(scope='session')
def edge_connection(edge):
    # Just to keep backward compatibility
    yield edge


@pytest.fixture(scope='function')
def check_edge_status(edge):
    """
    Check edge status
    :param edge: Edge connection fixture
    """
    if not edge.wait_for_connected():
        AssertionError('Edge not connected in cloud. Status: {}'.format(edge.read_status_api()))


@pytest.fixture(scope='class')
def edge_internal_id(edge):
    """
    Get edge internal id
    :param edge: Edge connection fixture
    """
    internal_id = edge.internal_id
    yield internal_id
    if internal_id:
        with open('internal.id', 'w') as f:
            f.write(internal_id)


@pytest.fixture(scope='session')
def kubectl(edge):  # pylint: disable=unused-argument
    return Kubectl()


@pytest.fixture(scope='class')
def kaas(kube_config_file_path):
    """
    Open connection to the kubernets as a service (KAAS) using kubernets python sdk
    :param kube_config_file_path: Kubernetes konfiguration file path
    :return: api_client
    """
    custom_configuration = Configuration()
    custom_configuration.assert_hostname = False
    load_kube_config(client_configuration=custom_configuration, config_file=kube_config_file_path)
    Configuration.set_default(custom_configuration)

    return Kaas(kube_config_file_path)


@pytest.fixture(scope='module')
def edge_cloud_api(tc_config_data):
    pelion_edge_cloud = PelionEdgeCloud(tc_config_data)
    yield pelion_edge_cloud


