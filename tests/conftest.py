import logging
import os
import uuid

import pytest


pytest_plugins = [
                  'pelion_systest_lib.fixtures.edge_fixtures',
                  'pelion_systest_lib.fixtures.general_fixtures',
                  'pelion_systest_lib.fixtures.iam_fixtures',
                  'pelion_systest_lib.fixtures.notification_fixtures'
]

log = logging.getLogger(__name__)

pytest.global_treasure_data = None
pytest.global_allocated_raas_resources = []
pytest.global_test_results = []
pytest.global_raas_usage = []


def pytest_addoption(parser):
    """
    Function for pytest to enable own custom commandline arguments
    :param parser: argparser
    :return:
    """
    parser.addoption('--config_path', action='store', help='Test case config json')
    parser.addoption('--api_gw', action='store', help='API gateway url')
    parser.addoption('--edge_k8s_url', action='store', help='Edge k8s url')
    parser.addoption('--gateways_url', action='store', help='Gateways url')
    parser.addoption('--show_api_key', action='store', help='true/false to show api keys on logs')
    parser.addoption('--no_summary', action='store_true', help='Does not collect the test result summary')


def pytest_report_teststatus(report, config):
    """
    Hook for collecting test results during the test run for the summary
    :param report: pytest test report
    :param config: argument configs
    :return:
    """
    error_rep = ''
    test_result = {'test_name': report.nodeid,
                   'result': report.outcome,
                   'when': report.when,
                   'duration': report.duration,
                   'error_msg': error_rep,
                   'jenkins_build_id': os.environ.get('BUILD_ID', ''),
                   'jenkins_job_url': os.environ.get('JOB_URL', ''),
                   'uuid': str(uuid.uuid4()),
                   'exitcode': '',
                   'jenkins_job_name': os.environ.get('JOB_NAME', ''),
                   'cloud_client_rel': os.environ.get('MBED_CLOUD_CLIENT_RC_REL', ''),
                   'cloud_environment': '',
                   'test_category': ''}
    if report.outcome == 'failed':
        if report.longrepr:
            for line in str(report.longrepr).splitlines():
                if line.startswith('E       '):
                    error_rep += '{}\n'.format(line)
            # this next one (hopefully) adds always the failing code line from pytest report
            error_rep += '{}\n'.format(str(report.longrepr).splitlines()[-1])
        test_result['error_msg'] = error_rep
        if not config.getoption('no_summary') or config.getoption('td_results'):
            if report.when == 'teardown':
                pytest.global_test_results.pop()

            pytest.global_test_results.append(test_result)
    else:
        if report.when == 'call':
            if not config.getoption('no_summary') or config.getoption('td_results'):
                pytest.global_test_results.append(test_result)

    if pytest.global_allocated_raas_resources and config.getoption('td_results'):
        raas_result = {'uuid': test_result['uuid'],
                       'raas_resources': pytest.global_allocated_raas_resources,
                       'test_name': test_result['test_name']}
        if report.outcome == 'failed' and report.when in ('setup', 'call'):
            pytest.global_raas_usage.append(raas_result)

        if report.outcome == 'passed' and report.when == 'call':
            pytest.global_raas_usage.append(raas_result)


def pytest_sessionfinish(session, exitstatus):
    """
    Hook for writing the test result summary to console log and TD database after the test run
    :param session:
    :param exitstatus:
    :return:
    """
    log.info('-----  TEST RESULTS SUMMARY  -----')
    log.info('[ check the complete fail reasons and code locations from this log or html report ]')
    for resp in pytest.global_test_results:
            result = resp['result']
            if result == 'failed':
                result = result.upper()
            log.info('[{}] - {} - ({:.3f}s)'.format(result, resp['test_name'], resp['duration']))
            if resp['error_msg'] != '':
                take_these = 3
                for line in resp['error_msg'].splitlines():
                    if take_these > 0:
                        log.info(line)
                    else:
                        log.info('E ---8<--- Error log summary cut down to few lines, '
                                 'check full log above or from html report ---8<---\n')
                        break
                    take_these -= 1




