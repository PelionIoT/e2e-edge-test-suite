import logging
import pytest

log = logging.getLogger(__name__)


def test_remote_terminal(edge):
    if not edge.has_remote_terminal:
        pytest.skip('Skipping because build don\'t have remote terminal')

    response = None
    try:
        response = edge.execute_remote_terminal('date +%A')
    except BaseException as e:
        log.info('Cannot execute using remote terminal: {}'.format(e))

    weekdays = ['Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday']

    assert response in weekdays, 'Remote terminal connection not working correctly'
