from dewarupdates.monitor import PuckTrackerMonitor
import pytest
from unittest.mock import MagicMock, call, patch


@pytest.yield_fixture
def monitor():
    yield PuckTrackerMonitor('localhost', 3000, 'http://templates')


def test_on_action_dispatches_by_type(monitor):
    monitor.on_do_something = MagicMock()
    monitor.on_action({'type': 'DO_SOMETHING', 'value': 123})
    assert monitor.on_do_something.call_args == call(value=123)


def test_on_action_does_nothing_if_callback_doesnt_exist(monitor):
    monitor.on_action({'type': 'UNHANDLED_ACTION'})


def test_on_action_handles_no_type(monitor):
    monitor.on_action({})


def test_on_update_dewar(monitor):
    action = {
        'type': 'UPDATE_DEWAR',
        'dewar': 'd-123a-1',
        'update': {'onsite': True},
    }
    with patch('dewarupdates.printer.print_page') as print_page:
        monitor.on_action(action)
        url = 'http://templates/arrival-slip/d-123a-1'
        assert print_page.call_args == call(url)
