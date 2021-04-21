# E2E Edge Test Suite

This is the Python test suite for Pelion Edge end-to-end tests. The library is designed to be used with
the [pytest test framework](https://docs.pytest.org/en/latest/).

## Prerequisites

* Python 3.6 or later.
* pip.
* venv (recommended).

```bash
sudo apt install python3-pip
sudo apt install python3-venv
```
## Setup

1. Clone repository.
1. Create virtual environment.
1. Upgrade pip.
1. Install requirements.

```bash
git clone https://github.com/PelionIoT/pelion-e2e-python-test-library.git
cd pelion-e2e-python-test-library
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

## Configure

1. Start Edge device.
1. Create configuration file based on environment config template:
    * [config_template_us.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_us.json).
    * [config_template_eu.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_eu.json).
    * [config_template_jp.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_jp.json).
1. Log in to the Pelion Device Management portal:
    * [portal.mbedcloud.com](https://portal.mbedcloud.com).
    * [portal-eu.mbedcloud.com](https://portal-eu.mbedcloud.com/).
    * [portal-jp.mbedcloud.com](https://portal-jp.mbedcloud.com/).
      
1. Create an access key in the portal.
1. Set the key in the configuration file.
1. Set the edge device ID in the configuration file.

### Example configuration file (EU):

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

## Run test

Run all tests:

```bash
pytest  --config_path=tests/config.json  --html=results.html

```

### Customized test runs

There are many ways to configure the test runs. Refer to the [full pytest documentation](https://docs.pytest.org/en/latest/contents.html) for more information.


## Current tests
### test_device_attributes.py 

Device attribute tests use Pelion Device Management [device directory APIs](https://developer.pelion.com/docs/device-management-api/device-directory/) to get device information and device attributes, such as registration status. 


 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_device_registered          | Verify the device is registered.                      |                              |

### test_k8s_kubectl.py

Kubernetes tests use the Kubernetes command-line tool, kubectl, to run commands against Kubernetes clusters.
Edge Kubernetes must be enabled in your Pelion Device Management account to run these tests successfully.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_node                       | Verify the device is registered in Kubernetes.        |                              |
| test_pod                        | Verify the test Pod can be launched.                  |                              |
| test_pod_state                  | Verify the test Pod state is running.                 |                              |


### test_lwm2m_resource.py

LwM2M resource tests use the [Pelion Device Management Connect API](https://developer.pelion.com/docs/device-management-api/connect/)
to read and write resource values to and from the device.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_put_lifetime               | Verify the write-to-device resource works.            | Resource '1/0/1'             |
| test_get_lifetime               | Verify the read-from-device resource works.           | Resource '1/0/1'             |


### test_remote_terminal.py 

These tests verify the device remote terminal is functional.

Note: Not all edge gateway devices have remote terminal supported.
Use the configuration file parameter `has_remote_terminal` to define if this test is part of the set.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_remote_terminal            | Verify communication via remote terminal works.       |                              |

### test_websocket_notificatios.py 

This test file tests uses [Pelion Device Management Notifications API](https://developer.pelion.com/docs/device-management-api/notifications/)
to register a websocket notification channel to receive notifications such as:
registration, registration update and resource notifications from the device.

 Test name                                | Main functions                                                      | Notes                        |
| ----------------------------------------| --------------------------------------------------------------------| -----------------------------|
| test_registration_update_notification   | Verify the registration update notification is received.            |                              |
| test_registration_notification          | Verify the registration notification is received after reboot.      |                              |
| test_notification_device_cpu_usage      | Verify the notification from the device is received.                | Resource: '/3/0/3320'        | 

## License

For licensing details, see the [license](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/LICENSE) agreement.
