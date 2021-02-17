"""
Edge KaaS kubectl related helper functions
"""

import logging
import os
import stat
import tempfile
import time

from jinja2 import Template

from pelion_systest_lib.tools import execute_local_command, build_random_string

log = logging.getLogger(__name__)


class Kubectl:
    kube_config_template = """
    apiVersion: v1
    clusters:
    - cluster:
        server: {{server}}
      name: edge-k8s
    contexts:
    - context:
        cluster: edge-k8s
        user: edge-k8s
        namespace: default
      name: edge-k8s
    current-context: edge-k8s
    kind: Config
    preferences: {}
    users:
    - name: edge-k8s
      user:
        token: {{api_key}}
    """

    def _write_config(self, folder, server_url, api_key, file_name='temporary_kubernetes_config.yaml'):
        kube_config_path = os.path.join(folder, file_name)
        try:
            with open(kube_config_path, 'w') as f:
                f.write(Template(self.kube_config_template).render(
                    server=server_url,
                    api_key=api_key))
        except:
            log.error('Cannot write file: {}'.format(kube_config_path))
            raise
        # Set 400 as pem permissions
        os.chmod(kube_config_path, stat.S_IRUSR)
        return kube_config_path

    def write_kubectl_config(self, server_url, api_key):
        try:
            # Try to write configuration in current directory first
            kube_config_path = self._write_config(os.getcwd(), server_url, api_key)
        except:  # pylint: disable=bare-except
            log.info('Cannot use current folder for kube config, using temp folder')
            # Use also custom name, to make this work more reliable
            kube_config_path = self._write_config(tempfile.gettempdir(), server_url, api_key,
                                                  '{}_kube_config.yaml'.format(build_random_string(5)))

        # Take configuration in use
        log.debug('Kube config successfully added in {}'.format(kube_config_path))
        return kube_config_path

    @staticmethod
    def describe_node(edge_internal_id):
        return execute_local_command('kubectl describe nodes {}'.format(edge_internal_id))

    @staticmethod
    def view_config():
        return execute_local_command('kubectl config view')

    @staticmethod
    def get_clusters():
        return execute_local_command('kubectl config get-clusters')

    @staticmethod
    def get_contexts():
        return execute_local_command('kubectl config get-contexts')

    @staticmethod
    def describe_pod(pod_name):
        return execute_local_command('kubectl describe pod {}'.format(pod_name))

    @staticmethod
    def get_pods():
        return execute_local_command('kubectl get pods')

    @staticmethod
    def get_pod(pod):
        return execute_local_command('kubectl get pods {}'.format(pod))

    @staticmethod
    def delete_pod(pod_name):
        return execute_local_command('kubectl delete pods {}  --force --grace-period=0'.format(pod_name))

    @staticmethod
    def pod_logs(pod_name):
        return execute_local_command('kubectl logs {}'.format(pod_name))

    @staticmethod
    def create_pod(pod_yaml_file):
        return execute_local_command('kubectl create -f {}'.format(pod_yaml_file))

    @staticmethod
    def manipulate_simple_pod_yaml(pod_yaml, edge_internal_id, pod_name):
        with open(pod_yaml, 'r') as f:
            data = f.read()
            original_data = data
            if 'ReplaceNodeName' in data:
                data = data.replace('ReplaceNodeName', edge_internal_id)
            if 'ReplacePodName' in data:
                data = data.replace('ReplacePodName', pod_name)
        with open(pod_yaml, 'w') as f:
            f.write(data)
        return original_data

    @staticmethod
    def execute_with_retry(command, assert_text, retry_count=20,
                           delay_in_sec=5):
        response = ''
        for i in range(retry_count + 1):
            if i > 0:
                log.info('{}/{} retry: {}'.format(i, retry_count - 1, command))
            response = execute_local_command(command, False)
            if assert_text in response:
                break
            time.sleep(delay_in_sec)
        return response

    def get_node(self, edge_internal_id, expected_status, retry_count=30, delay_in_sec=5):
        response = self.execute_with_retry(command='kubectl get node {}'.format(edge_internal_id),
                                           assert_text=expected_status, retry_count=retry_count,
                                           delay_in_sec=delay_in_sec)
        return response
