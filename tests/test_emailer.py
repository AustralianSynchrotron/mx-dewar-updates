from dewarupdates import emailer
import pytest
from mailshake import ToMemoryMailer
import os


@pytest.yield_fixture
def mailer():
    yield ToMemoryMailer()


@pytest.yield_fixture
def dewar():
    yield {
        'name': 'd-123a-1',
        'epn': '123a',
        'owner': 'Jane',
        'institute': 'Some University',
        'note': 'Keep onsite',
        'containerType': 'pucks',
        'expectedContainers': 'ASP001,ASP002',
        'onsite': True,
        'department': 'Chemistry',
        'streetAddress': '1 Main Rd',
        'city': 'Melbourne',
        'state': 'VIC',
        'postcode': '3000',
        'country': 'Australia',
        'phone': '123-456-789',
        'email': 'jane@example.com',
        'returnDewar': True,
        'courier': 'Fast Deliveries',
        'courierAccount': '122333',
        'addedTime': "2016-02-10T09:00:00Z",
        'arrivedTime': "2016-02-14T11:31:37.183Z",
        'departedTime': None,
        'experimentStartTime': "2016-02-15T08:00:00Z",
        'experimentEndTime': "2016-02-15T16:00:00Z",
        'filledTime': None,
    }


def test_send_arrival_email(dewar, mailer):
    os.environ['DEWAR_UPDATES_CC'] = 'someone@example.com,someone.else@example.com'
    emailer.send_arrival_email(dewar, mailer)
    assert len(mailer.outbox) == 1
    email = mailer.outbox[0]
    expected_subject = ('Your dewar with ID d-123a-1 has arrived at '
                        'the Australian Synchrotron')
    assert email.subject == expected_subject
    assert 'is now at the MX beamlines' in email.text
    assert 'd-123a-1' in email.text
    assert email.from_email == 'mxlabs@synchrotron.org.au'
    assert 'jane@example.com' in email.to
    assert 'someone@example.com' in email.cc
    assert 'someone.else@example.com' in email.cc


def test_send_departed_email(dewar, mailer):
    emailer.send_departed_email(dewar, mailer)
    email = mailer.outbox[0]
    expected_subject = ('Your dewar with ID d-123a-1 is ready to depart from the '
                        'Australian Synchrotron').format(dewar['name'])
    assert email.subject == expected_subject
    assert 'left the beamline' in email.text
    assert 'd-123a-1' in email.text


def test_send_filled_email(dewar, mailer):
    emailer.send_filled_email(dewar, mailer)
    email = mailer.outbox[0]
    expected_subject = ('Your dewar with ID d-123a-1 has been filled with '
                        'liquid nitrogen' )
    assert email.subject == expected_subject
    assert 'topped up with liquid nitrogen' in email.text
    assert 'd-123a-1' in email.text


def test_send_filled_email(dewar, mailer):
    emailer.send_missing_email(dewar, mailer)
    email = mailer.outbox[0]
    expected_subject = ('Please advise the Australian Synchrotron of the status '
                        'of your dewar')
    assert email.subject == expected_subject
    assert 'has not been able to find it' in email.text
    assert 'd-123a-1' in email.text
