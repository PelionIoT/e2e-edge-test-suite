# Izuma E2E Edge Python Test Suite Change log

## 1.2.1
- Add marker `reboot_test` to LwM2M test that resets device. This allows you to skip that test with `pytest -m "not reboot_test"`.

## 1.2.0
- Python 3.10 warning removal by creating eventloop explicitly.
- New test file for checking edge device being on-line ([tests/test_edge_online.py](test/test_edge_online.py)).
- Fix deprecation warning in `websocket_handler.py` (setDaemon() is deprecated).

## 1.1.0  2022-Sep-01
- Izuma branding changes.
- Remove EU and JP config templates.
- Fix license link.
- Fix Jenkinsfile link.
- Update requirements.txt to work better with Python 3.10.

## 1.0.0  2021-Mar-04
- Initial release of Pelion E2E Edge Python Test Suite
