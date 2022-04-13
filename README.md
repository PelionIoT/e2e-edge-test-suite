# E2E Edge Test Suite

This is the Python test suite for Pelion Edge end-to-end tests. The library is designed to be used with
the [pytest test framework](https://docs.pytest.org/en/latest/).

<h1 id="end-to-end">End-to-end Edge Test Suite</h1>

You can perform end-to-end tests using the [Python test suite for Pelion Edge end-to-end tests](https://github.com/PelionIoT/e2e-edge-test-suite/blob/main/README.md). The library is designed to be used with the [pytest test framework](https://docs.pytest.org/en/latest/).

## Prerequisites

Before you can use the end-to-end test suite, you must have:

- Python 3.6 or later.
- pip.
- venv (recommended).

```bash
sudo apt install python3-pip
sudo apt install python3-venv
```

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/).

   Example:

   ```bash
   snap install kubectl --classic
   kubectl version --client
   ```

## Set up

1. Clone repository.
1. Create virtual environment.
1. Upgrade pip.
1. Install requirements.

```bash
git clone https://github.com/PelionIoT/e2e-edge-test-suite.git
cd e2e-edge-test-suite
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Configure

1. Start Edge device.
1. Create a configuration file based on the environment config template:

   - [config_template_us.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_us.json).
   - [config_template_eu.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_eu.json).
   - [config_template_jp.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_jp.json).

1. Log in to the Pelion Device Management portal:

   - [portal.mbedcloud.com](https://portal.mbedcloud.com).
   - [portal-eu.mbedcloud.com](https://portal-eu.mbedcloud.com/).
   - [portal-jp.mbedcloud.com](https://portal-jp.mbedcloud.com/).

1. [Create an access key](https://developer.pelion.com/docs/device-management/current/user-account/application-access-keys.html) in the portal.
1. Set the key in the configuration file.
1. Set the edge device ID in the configuration file.

Example configuration file (EU):

```json
{
  "api_gw": "https://api.eu-west-1.mbedcloud.com",
  "api_key": "",
  "connection_type": "cloud",
  "edge_k8s_url": "https://edge-k8s.eu-west-1.mbedcloud.com",
  "gateways_url": "https://gateways.eu-west-1.mbedcloud.com",
  "device_id": "",
  "has_remote_terminal": true
}
```

## Run

Run all tests:

```bash
pytest  --config_path=tests/config.json  --html=results.html

```

### Customize

There are many ways to configure the test runs. Refer to the [full pytest documentation](https://docs.pytest.org/en/latest/contents.html) for more information.

## Tests

### test_device_attributes.py

Device attribute tests use Pelion Device Management [device directory APIs](https://developer.pelion.com/docs/device-management-api/device-directory/) to get device information and device attributes, such as registration status.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_device_registered          | Verify the device is registered.                      |                              |

### test_k8s_kubectl.py

Kubernetes tests use the Kubernetes command-line tool, kubectl, to run commands against Kubernetes clusters. You must enable Edge Kubernetes in your Pelion Device Management account to run these tests successfully.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_node                       | Verify the device is registered in Kubernetes.        |                              |
| test_pod                        | Verify the test Pod can be launched.                  |                              |
| test_pod_state                  | Verify the test Pod state is running.                 |                              |

### test_lwm2m_resource.py

LwM2M resource tests use the [Pelion Device Management connect API](https://developer.pelion.com/docs/device-management-api/connect/)
to read and write resource values to and from the device.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_put_lifetime               | Verify the write-to-device resource works.            | Resource '1/0/1'             |
| test_get_lifetime               | Verify the read-from-device resource works.           | Resource '1/0/1'             |

### test_remote_terminal.py

These tests verify the device remote terminal is functional.

<span class="notes">**Note:** Not all edge gateway devices have remote terminal supported. Use the configuration file parameter `has_remote_terminal` to define whether this test is part of the set.</span>

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_remote_terminal            | Verify communication via remote terminal works.       |                              |

### test_websocket_notifications.py

This test file uses the [Pelion Device Management notifications API](https://developer.pelion.com/docs/device-management-api/notifications/) to register a websocket notification channel to receive notifications such as registration, registration update and resource notifications from the device.

 Test name                                | Main functions                                                      | Notes                        |
| ----------------------------------------| --------------------------------------------------------------------| -----------------------------|
| test_registration_update_notification   | Verify the registration update notification is received.            |                              |
| test_registration_notification          | Verify the registration notification is received after reboot.      |                              |
| test_notification_device_cpu_usage      | Verify the notification from the device is received.                | Resource: '/3/0/3320', supported by Snap-Pelion-Edge|

## License

For licensing details, please see the [license](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/LICENSE) agreement.
