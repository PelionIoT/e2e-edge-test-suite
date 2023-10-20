# Izuma E2E Edge Python Test Suite Change log

## 1.2.1
- Add marker `cpu_notif_test` to CPU resource notification test. This allows you to skip that test with `pytest -m "not cpu_notif_test"`. You can skip that and reboot test with `-m 'not (reboot_test or cpu_notif_test)'`.
- Add marker `reboot_test` to LwM2M test that resets device. This allows you to skip that test with `pytest -m "not reboot_test"`.
- Move `pytest.ini` from `tests`-folder to root, this way to the custom marker gets taken into account.
- Upgrade `pytest` to 7.3.1 and `pytest-html` 3.2.0 to resolve Python 3.10 compatibility issue.
- Add *.xml files to `.gitignore`.

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
