# ----------------------------------------------------------------------------
# Copyright (c) 2023, Izuma Networks
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

# ----------------------------------------------------------------------------
# This test file tests use edge device is online,
# - LwM2M connectivity (via reading /3/0/13 - i.e. epoch time)
# - Kubectl node status being Ready
# - Remote terminal working as well.
#
# Edge K8S must be enabled in your Izuma account to run these test
# successfully.
#
# You must have a working kubectl configuration in $HOME/.kube/config.
# - You can confirm that by running kubectl get nodes
# ----------------------------------------------------------------------------

import logging
import time
import pytest
import json

from izuma_systest_lib.cloud import connect_handler
from izuma_systest_lib.tools import execute_local_command


KUBECLT_GET_NODES = "kubectl get nodes -o=json"

log = logging.getLogger(__name__)


def test_LwM2M_OK(edge, cloud_api, websocket):
    """
    Verify if LwM2M connection is OK to devicey by reading epoch time resource.

    :param edge:        edge structure with device ID etc.
    :param cloud_api:   cloud API struct
    :param websocket:   websocket for async notifications
    """

    resource = '/3/0/13'
    payload = {'method': 'GET', 'uri': resource}
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)
    # Test response received with 200 OK status
    assert resp and resp['status'] == 200, 'Unable to read device resource: {} value'.format(resource)
    epoch_received = float(resp.get('decoded_payload'))
    log.debug("Received /3/0/13 epoch time {epoch_received}.")
    time.sleep(10)
    resp = connect_handler.send_async_device_and_wait_for_response(cloud_api,
                                                                   channel_type=websocket,
                                                                   ep_id=edge.device_id,
                                                                   apikey=websocket.api_key,
                                                                   payload=payload, async_id=None)
    # Test response received with 200 OK status
    assert resp and resp['status'] == 200, 'Unable to read device resource: {} value'.format(resource)
    epoch_received_10s_later = float(resp.get('decoded_payload'))
    epoch_delta = epoch_received_10s_later - epoch_received
    log.debug("Received /3/0/13 epoch time {epoch_received} 10 s later.")
    assert epoch_delta >= 10, f"Epoch time delta {epoch_delta} not >= 10 s."


def test_Kube_is_OK(edge):
    """
    Verify if Edge Kubernetes is in Ready -state.

    :param edge:    Edge -structure
    """

    kubectl_get_nodes = execute_local_command(KUBECLT_GET_NODES)
    json_data = json.loads(kubectl_get_nodes)
    for i in json_data["items"]:
        name = i["metadata"]["name"]
        if name == edge.device_id:
            for j in i["status"]["conditions"]:
                reason = j["reason"]
                status = j["status"]
                type = j["type"]
                log.debug(
                    f"j[reason]='{reason}', "
                    f"j[type]='{type}', "
                    f"j[status]='{status}'"
                )
                if reason == "KubeletReady" and type == "Ready":
                    assert status == "True", "Not status not Ready"
                    return
        else:
            log.debug(f"Non-matching device {name}.")
    print(
        f"ERROR - can't find device ID {edge.device_id} from kubectl "
        f"get nodes output."
    )
    assert False, f"ERROR - can't find device ID {edge.device_id} from kubectl get nodes."


def test_Terminal_OK(edge):
    """
    Verify if Edge Terminal is responding to echo command.

    :param edge:    Edge -structure
    """
    if not edge.has_remote_terminal:
        pytest.skip("Skipping because device does not have remote terminal supported.")

    assert "terminal_is_alive" == edge.execute_remote_terminal("echo terminal_is_alive"), "Remote terminal not OK."


def test_Edge_Online(edge, cloud_api, websocket):
    """
    Verify if Edge is online using the 3 tests above.

    You can run this test in repeat:

    pytest --count=10 --config_path=config-rpi3.json tests/test_edge_online.py::test_Edge_Online

    :param edge:        edge structure with device ID etc.
    :param cloud_api:   cloud API struct
    :param websocket:   websocket for async notifications
    """

    test_LwM2M_OK(edge, cloud_api, websocket)
    test_Terminal_OK(edge)
    test_Kube_is_OK(edge)
