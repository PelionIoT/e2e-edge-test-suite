"""
This file helps tests writing for KaaS (Kubernetes as a service)
"""

import inspect
import logging
from os.path import abspath, dirname, join
from time import time, sleep

import yaml
from jinja2 import Template
from kubernetes.client import Configuration, CoreV1Api, StorageV1Api, V1DeleteOptions, V1Node, V1ObjectMeta, AppsV1Api
from kubernetes.client.api_client import ApiClient
from kubernetes.client.rest import ApiException
from kubernetes.config import load_kube_config
from kubernetes.stream import stream
from kubernetes.utils import create_from_yaml
from kubernetes.utils.create_from_yaml import FailToCreateError

log = logging.getLogger(__name__)


class Kaas:

    def __init__(self, kube_config_file_path):
        """
        Initialize with default values if not defined
        Note: Need to initialize parameters in test side to make this working. Not sure for reason.
        Parameters are initialized here to give tip for IDE which kind of classes those are.
        :param k8s_client: Kubernetes api client
        :param corev1: corev1 api client
        :param storage_class: storage class api client
        :param daemon: daemonset  api client
        """
        load_kube_config(config_file=kube_config_file_path)
        self.corev1 = CoreV1Api()
        self.storage_class = StorageV1Api()
        self.k8s_client = ApiClient(Configuration())
        self.daemon = AppsV1Api(ApiClient())

    @staticmethod
    def _error(explanation, error):
        log.debug('{} Error: {}'.format(explanation, error))
        raise Exception('Edge KaaS problem, {}! See debug logs for details'.format(explanation))

    def create_from_yaml(self, yaml_file, throw_err=True):
        """
        function to create KAAS (kubernets as a service) resources required for the tests
        :param yaml_file: yaml file which
        :param throw_err: this can be either True or False. If the value passed is True then test will fail and exception will be
        thrown, if value passed is False then exception will be caught and passed to user for verification this is useful in case
        of negative tests where we know we are passing a wrong value and want to validate correct exception message is thrown
        """
        try:
            return create_from_yaml(self.k8s_client, yaml_file)
        except FailToCreateError as e:
            if not throw_err:
                return e
            self._error('Cannot create kubernetes resources from yaml.', e)
        except BaseException as e:
            self._error('Cannot create kubernetes resources from yaml.', e)

    @staticmethod
    def get_yaml_template(data_folder='', file_name=''):
        """
        function to return test yaml template it can be used in two ways
        1)if the values for data folder and filename are provided then it will join the two and take the data from that file
        2)if values for data folder and filename are not provided then it will automatically look for a data file in folder
        called data which is present a folder level which houses test script
        :param data_folder: relative location of data folder. Default ../data
        :param file_name: name of data file. Default is python module name but .yaml postfix
        :return:
        """
        try:
            frm = inspect.stack()[1]
            module = inspect.getmodule(frm[0])
            base_script_dir = dirname(module.__file__)
            if not file_name:
                file_name = module.__name__ + '.yaml'

            # Make data_folder as absolute path
            if not data_folder:
                data_folder = abspath(join(base_script_dir, '..', 'data'))
            else:
                data_folder = abspath(join(base_script_dir, data_folder))

            with open(join(data_folder, file_name)) as f:
                template = Template(f.read())
                return template
        except BaseException as e:
            Kaas._error('Cannot read yaml data file.', e)

    def wait_for_pod_state_change(self, pod_name, state='Pending', timeout=200, namespace='default'):
        """
        function to wait for state of pod to change (this can be used to check if pod is ready by keeping state as pending or can
        be used to check if pod has been deleted by keeping the state as Running)
        :param pod_name: name of pod
        :param state: state of pod to be validated
        :param timeout: timeout in seconds
        :param namespace: pods namespace
        """
        start_time = time()
        log.info('Waiting for pod: {} state to change..'.format(pod_name))
        while True:
            read_pod_resp = self.corev1.read_namespaced_pod(name=pod_name, namespace=namespace)
            phase = read_pod_resp.status.phase
            log.info('Pod current state {}'.format(phase))
            if phase != state:
                if state == 'Running' and phase == 'Pending':
                    # this handles situation where while deleting a pod at times it moves from Running to Pending for a split
                    # second
                    sleep(5)
                else:
                    break

            if time() - start_time >= timeout:
                raise Exception(
                    'Pod: {} state change Failed. State did not change {} seconds.'.format(pod_name, timeout))

            # Waiting between loops, because it takes some time for pod state to change
            sleep(10)
        log.info('Pod: {}, change successful'.format(pod_name))

    def create_pod(self, yaml_str, namespace='default'):
        """
        Create a pod from yaml syntax
        :param yaml_str: pod yaml in string
        :param namespace: pod namespace
        :return:
        """
        body = yaml.safe_load(yaml_str)
        try:
            return self.corev1.create_namespaced_pod(namespace=namespace, body=body)
        except ApiException as e:
            log.debug('Edge KaaS problem, Cannot create pod. Error: {}'.format(e))
            raise Exception('Cannot create pod. Reason: {}'.format(e.reason))
        except BaseException as e:
            self._error('Cannot create pod.', e)

    def read_namespaced_pod(self, name, namespace='default'):
        """
        Masking CoreV1Api.read_namespaced_pod() function to make it calling easier in test case side
        :param name: Pod name
        :param namespace: namespace for the pod
        :return:
        """
        try:
            return self.corev1.read_namespaced_pod(name, namespace)
        except BaseException as e:
            self._error('Cannot read pod.', e)

    def read_namespaced_pod_status(self, name, namespace='default'):
        """
        Read namespaced pod status
        :param name: Pod name
        :param namespace: namespace for the pod
        :return:
        """
        try:
            return self.corev1.read_namespaced_pod_status(name, namespace)
        except BaseException as e:
            self._error('Cannot read pod status.', e)

    def read_pod_log(self, name, namespace='default'):
        """
        Read pod logs
        :param name: Pod name
        :param namespace: namespace for the pod
        :return:
        """
        try:
            return self.corev1.read_namespaced_pod_log(name, namespace)
        except BaseException as e:
            self._error('Cannot read pod.', e)

    def execute_command_on_pod(self, pod_name, shell_command, container_name, namespace='default'):
        """
        function to execute command on KAAS (kubernets as a service) pod
        :param pod_name: name of pod
        :param shell_command: command which has to be executed
        :param container_name: name of pod container used to trigger shell
        :param namespace: namespace for the pod
        """
        command = ['/bin/sh', '-c', shell_command]
        try:
            pod_exec_response = stream(self.corev1.connect_get_namespaced_pod_exec, pod_name, namespace,
                                       command=command,
                                       container=container_name,
                                       stderr=True,
                                       stdin=False,
                                       stdout=True,
                                       tty=False)
            return pod_exec_response.rstrip()
        except BaseException as e:
            self._error('Cannot execute command on pod.', e)

    def pod_is_deleted(self, pod_name):
        """
        Check that pod is deleted and cannot access anymore
        :param pod_name: name of the pod
        :return:
        """
        try:
            self.wait_for_pod_state_change(pod_name=pod_name, state='Running')
        except ApiException as exception_object:
            if exception_object.status == 404:
                log.info('Delete successful')
                return True
            log.error('Unknown error: {}'.format(exception_object))
        return False

    def delete_namespaced_persistent_volume_claim(self, name):
        """
        Masking CoreV1Api.delete_namespaced_persistent_volume_claim() function
        to make it calling easier in test case side
        :param name: Persistent volume claim name
        :return:
        """
        try:
            return self.corev1.delete_namespaced_persistent_volume_claim(
                name=name,
                namespace='default',
                body=V1DeleteOptions(),
                grace_period_seconds=0)
        except BaseException as e:
            self._error('Cannot delete persistent volume claim.', e)

    def delete_pods(self, pod_names, namespace='default'):
        """
        Function to delete pods
        :param pod_names: name of pods to be deleted if more than one pod is given each name should be followed by space
        :param namespace: namespace for which pods have to be deleted
        """
        log.info('Deleting pods..')
        for pod_name in pod_names.split():
            self.delete_pod(pod_name, namespace)

    def delete_pod(self, name, namespace='default'):
        """
        Function to delete pods
        :param name: name of pod to be deleted
        :param namespace: namespace for which pods have to be deleted
        """
        log.info('Deleting pod: {}'.format(name))
        try:
            return self.corev1.delete_namespaced_pod(
                name=name,
                namespace=namespace,
                body=V1DeleteOptions(),
                grace_period_seconds=0)
        except BaseException as e:
            self._error('Cannot delete pod.', e)

    def delete_pvc(self, pvc_name, namespace='default'):
        """
        Function to delete persistent volume claim
        :param pvc_name: name of persistent volume claim to be deleted if more than one is given
        each name should befollowed by space
        :param namespace: namespace for for which pods have to be deleted
        """
        log.info('Deleting persistent volume claim ..')
        for name in pvc_name.split():
            try:
                self.corev1.delete_namespaced_persistent_volume_claim(
                    name=name,
                    namespace=namespace,
                    body=V1DeleteOptions(),
                    grace_period_seconds=0)
            except BaseException as e:
                self._error('Cannot delete persistent volume claim.', e)

    def read_namespaced_persistent_volume_claim(self, name, namespace='default'):
        """
        Read persistent volume claim
        :param name: name of volume claim
        :param namespace: used namespace
        :return:
        """
        log.info('Reading persistent volume claim: {}'.format(name))
        try:
            return self.corev1.read_namespaced_persistent_volume_claim(
                name=name,
                namespace=namespace)
        except BaseException as e:
            self._error('Cannot read namespaced persistent volume claim.', e)

    def delete_sc(self, sc_name):
        """
        Function to delete storage class
        :param sc_name: name of storage class to be deleted if more than one is specified
        each name should be followed by space
        """
        log.info('Deleting storage class %s', sc_name)
        for name in sc_name.split():
            try:
                self.storage_class.delete_storage_class(
                    name=name,
                    body=V1DeleteOptions(),
                    grace_period_seconds=0)
            except BaseException as e:
                self._error('Cannot delete storage class.', e)

    def delete_persistent_volume(self, name):
        """
        Delete persistent volume claim
        :param name: Persistent volume claim name
        :return: V1Status
                 If the method is called asynchronously,
                 returns the request thread.
        """
        log.info('Delete persistent volume claim: {}'.format(name))
        try:
            return self.corev1.delete_persistent_volume(
                name=name,
                body=V1DeleteOptions(),
                grace_period_seconds=0)
        except BaseException as e:
            self._error('Cannot delete persistent volume.', e)

    def update_node_label(self, name, label_name, label_value):
        """
        Function to update label of node
        :param name: name of node to be updated
        :param label_name: name of label to be updated
        :param label_value: updated value of label
       """
        log.debug('Delete persistent volume claim: {}'.format(name))
        try:
            node_body = V1Node()
            node_metadata = V1ObjectMeta(labels={label_name: label_value})
            node_body.metadata = node_metadata
            self.corev1.patch_node(name, node_body)
        except BaseException as e:
            self._error('Cannot update node label', e)

    def get_daemon_pod_name(self, daemonset_name, timeout=100):
        """
        Function to get daemon pod name
        and return AppsV1Api object for daemonsets manipulation
        :param daemonset_name: name of daemonset for which pod has to be found
        :param timeout: maximum timeout allowed
        :return: daemon_pod_name
        """
        try:
            daemon_pod_name = ''
            start_time = time()
            while True:
                pod_list = self.corev1.list_namespaced_pod(namespace='default',
                                                           label_selector='name={}'.format(daemonset_name))
                log.debug('Looking for pods for daemon {}'.format(daemonset_name))
                for pods in pod_list.items:
                    daemon_pod_name = pods.metadata.name
                if daemon_pod_name != '':
                    break
                if time() - start_time > timeout:
                    raise Exception('Timeout: Cannot find daemon pod in {} seconds'.format(timeout))
                sleep(5)
            return daemon_pod_name
        except BaseException as e:
            self._error('Cannot find daemon pod', e)

    def delete_configmaps(self, cm_names, namespace='default'):
        """
        Function to delete configmaps
        :param cm_names: name of config maps to be deleted if more than one pod is given each name should be followed by space
        :param namespace: namespace for which pods have to be deleted
        """
        log.info('Deleting configmaps..')
        for configmap in cm_names.split():
            self.delete_configmap(configmap, namespace)

    def delete_configmap(self, name, namespace='default'):
        """
        Function to delete configmap
        :param name: name of configmap to be deleted
        :param namespace: namespace for which configmap has to be deleted
        """
        log.info('Deleting configmap: {}'.format(name))
        try:
            return self.corev1.delete_namespaced_config_map(
                name=name,
                namespace=namespace,
                body=V1DeleteOptions(),
                grace_period_seconds=0)
        except BaseException as e:
            self._error('Cannot delete configmap.', e)

    def delete_secrets(self, secret_names, namespace='default'):
        """
        Function to delete secrets
        :param secret_names: name of secrets to be deleted if more than one pod is given each name should be followed by space
        :param namespace: namespace for which secrets have to be deleted
        """
        log.info('Deleting secrets..')
        for secret in secret_names.split():
            self.delete_secret(secret, namespace)

    def delete_secret(self, name, namespace='default'):
        """
        Function to delete secret
        :param name: name of secret to be deleted
        :param namespace: namespace for which secret has to be deleted
        """
        log.info('Deleting secret: {}'.format(name))
        try:
            return self.corev1.delete_namespaced_secret(
                name=name,
                namespace=namespace,
                body=V1DeleteOptions(),
                grace_period_seconds=0)
        except BaseException as e:
            self._error('Cannot delete secret.', e)

    def is_configmap_deleted(self, configmap_name, namespace='default'):
        """
        Check that configmap is deleted and cannot be access anymore
        :param configmap_name: name of the config map
        :param namespace: name of namespace for config map
        :return:
        """
        try:
            self.corev1.read_namespaced_config_map(configmap_name, namespace)
        except ApiException as exception_object:
            if exception_object.status == 404:
                log.debug('Delete successful')
                return True
            log.error('Unknown error while deleting config map: {}'.format(exception_object))
        return False

    def is_secret_deleted(self, secret_name, namespace='default'):
        """
        Check that secret is deleted and cannot be accessed anymore
        :param secret_name: name of the secret
        :param namespace: name of namespace for secret
        :return:
        """
        try:
            self.corev1.read_namespaced_secret(secret_name, namespace)
        except ApiException as exception_object:
            if exception_object.status == 404:
                log.debug('Delete successful')
                return True
            log.error('Unknown error while deleting secret: {}'.format(exception_object))
        return False
