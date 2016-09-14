import os
from jinja2 import Environment, FileSystemLoader


environment = Environment()
loader = FileSystemLoader('dewarupdates/templates')


def render_template(filename, **kwargs):
    return loader.load(environment, filename).render(**kwargs)


def send_email(subject, template, dewar, mailer):
    content = render_template(template, dewar=dewar)
    cc = os.environ.get('DEWAR_UPDATES_CC', '').split(',')
    mailer.send(
        subject=subject,
        text_content=content,
        from_email='mxlabs@synchrotron.org.au',
        to=[dewar['email']],
        cc=cc,
    )


def send_arrival_email(dewar, mailer):
    subject = ('Your dewar with ID {} has arrived at '
               'the Australian Synchrotron').format(dewar['name'])
    send_email(subject, 'arrival.txt', dewar, mailer)


def send_departed_email(dewar, mailer):
    subject = ('Your dewar with ID {} is ready to depart from the '
               'Australian Synchrotron').format(dewar['name'])
    send_email(subject, 'departed.txt', dewar, mailer)


def send_filled_email(dewar, mailer):
    subject = 'Your dewar with ID {} has been filled with liquid nitrogen'\
              .format(dewar['name'])
    send_email(subject, 'filled.txt', dewar, mailer)


def send_missing_email(dewar, mailer):
    subject = ('Please advise the Australian Synchrotron of the status '
               'of your dewar')
    send_email(subject, 'missing.txt', dewar, mailer)
