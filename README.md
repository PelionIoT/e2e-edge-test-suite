# E2E Edge Test Suite

<!-- nucloud:start -->
[![nucloud](https://github.com/PelionIoT/e2e-edge-test-suite/actions/workflows/nucloud.yml/badge.svg?branch=nucloud)](https://github.com/PelionIoT/e2e-edge-test-suite/actions/workflows/nucloud.yml)
[![nucloud branch](https://img.shields.io/badge/branch-nucloud-blue.svg)](https://github.com/IzumaNetworks/nucloud/blob/main/docs/standards.md)
[![production](https://img.shields.io/badge/production-pre--nucloud-lightgrey.svg)](https://github.com/PelionIoT/e2e-edge-test-suite/releases/tag/archive/pre-nucloud)

Build and deploy: [docs/nucloud.md](docs/nucloud.md).
<!-- nucloud:end -->


This is the Python test suite for Izuma Edge end-to-end tests. The library is designed to be used with
the [pytest test framework](https://docs.pytest.org/en/latest/).

For more information, please see the [public documentation](https://developer.izumanetworks.com/docs/device-management-edge/latest/testing/end-to-end.html).

## Running on nucloud

`make test MACHINE=staging ACCOUNT=edge` runs the suite against the gateway named in the edge env file. Without `SUITES` it leaves out the reboot case; `SUITES` takes test paths and pytest arguments, such as `SUITES=tests/test_lwm2m_resources.py`. The remote terminal opens `/v3alpha/devices/{id}/console` on the API host, and the Kubernetes cases call the env file's `edge_k8s_url`.

## License

For licensing details, see the [license](https://github.com/PelionIoT/e2e-edge-test-suite/blob/main/LICENSE) agreement.
