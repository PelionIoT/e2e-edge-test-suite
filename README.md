# Pelion E2E Edge Python Test Suite

Python test suite for Pelion Edge E2E tests The library is designed to be used with
the [pytest test framework](https://docs.pytest.org/en/latest/).

## Prerequisites

Python 3.5 or later.

## Setup

- Clone repository
- Create virtual environment
- Install requirements

```bash
$ git clone https://github.com/PelionIoT/pelion-e2e-python-test-library.git
$ cd pelion-e2e-python-test-library
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt

```

## Configure

- Start Edge device
- Create configuration file based on config_template.json
- Login Device management portal: https://portal.mbedcloud.com
    - Create access/api key in portal and set key in config file.
- Set Edge device id in config file.

```json
{
  "api_gw": "https://api.eu-west-1.mbedcloud.com",
  "api_key": "",
  "connection_type": "cloud",
  "edge_k8s_url": "https://edge-k8s.eu-west-1.mbedcloud.com",
  "gateways_url": "https://gateways.eu-west-1.mbedcloud.com",
  "device_id": "",
  "has_remote_terminal": true,
  "edge_skip_release": true,
  "edge_local_host_port": 9101
}
```

## Run test

```bash
$ pytest test_example.py --config_path=config_template.json

Adjust pytest arguments with logs details and generate html report
$ pytest test_example.py --config_path=config_template.json --log-cli-level=INFO --html=results.html
```

