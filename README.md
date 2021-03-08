# Pelion E2E Edge Python Test Suite

Python test suite for Pelion Edge E2E tests The library is designed to be used with
the [pytest test framework](https://docs.pytest.org/en/latest/).

## Prerequisites

* Python 3.6 or later.
* pip
* venv (recommended)

```bash
sudo apt install python3-pip
sudo apt install python3-venv
```
## Setup

* Clone repository
* Create virtual environment
* Upgrade pip and install requirements

```bash
git clone https://github.com/PelionIoT/pelion-e2e-python-test-library.git
cd pelion-e2e-python-test-library
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```

## Configure

* Start Edge device
* Create configuration file based on environment config template.
    * [config_template_us.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_us.json)
    * [config_template_eu.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_eu.json)
    * [config_template_jp.json](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/tests/config_template_jp.json)
* Login Device management portal:
    * [portal.mbedcloud.com](https://portal.mbedcloud.com)
    * [portal-eu.mbedcloud.com](https://portal-eu.mbedcloud.com/)
    * [portal-jp.mbedcloud.com](https://portal-jp.mbedcloud.com/)
      
* Create access key in portal and set key in configuration file.
* Set Edge Device Id in configuration file.

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

* Run all tests
```bash
pytest  --config_path=tests/config.json  --html=results.html

```

### Customized test runs

There are many ways to configure the test runs. Refer to the [full pytest documentation](https://docs.pytest.org/en/latest/contents.html) for more information.


## Current tests
### test_device_attributes.py 
Device attribute tests use Pelion device management [device directory API's](https://developer.pelion.com/docs/device-management-api/device-directory/) to get device information 
e.g. device attributes like registration status. 


 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_device_registered          | Verify that the device is registered.                 |                              |

### test_k8s_kubectl.py
K8s tests use The Kubernetes command-line tool, kubectl, to run commands against Kubernetes clusters.
Edge k8s must be enabled in your Pelion device management account to run these test successfully.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_node                       | Verify that the device is registered in k8s.          |                              |
| test_pod                        | Verify that the test pod can be launched.             |                              |
| test_pod_state                  | Verify that the test pod state is running.            |                              |


### test_lwm2m_resource.py
LwM2M resource tests use [Pelion connect API](https://developer.pelion.com/docs/device-management-api/connect/)
to read and write resource values from/to device.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_put_lifetime               | Verify that write to device resource works.           | Resource '1/0/1'             |
| test_get_lifetime               | Verify that read from device resource works.          | Resource '1/0/1'             |


### test_remote_terminal.py 
Verifying that device remote terminal is functional.

Note all edge/gateway devices may not have remote terminal supported.
Use configuration file parameter 'has_remote_terminal' to define if test is part of the set.

 Test name                        | Main functions                                        | Notes                        |
| ------------------------------- | ------------------------------------------------------| -----------------------------|
| test_remote_terminal            | Verify that communication vie remote terminal works.  |                              |

### test_websocket_notificatios.py 
This test file tests use [Pelion notifications API](https://developer.pelion.com/docs/device-management-api/notifications/)
to register websocket notification channel to receive notifications like:
registration, registration-update, resource notifications from the device.

 Test name                                | Main functions                                                      | Notes                        |
| ----------------------------------------| --------------------------------------------------------------------| -----------------------------|
| test_registration_update_notification   | Verify that the registration update notification is received.       |                              |
| test_registration_notification          | Verify that the registration notification is received after reboot. |                              |
| test_notification_device_cpu_usage      | Verify that the notification from device is received.               | Resource: '/3/0/3320'        | 

## License

See the [license](https://github.com/PelionIoT/pelion-e2e-edge-python-test-suite/blob/main/LICENSE) agreement.
