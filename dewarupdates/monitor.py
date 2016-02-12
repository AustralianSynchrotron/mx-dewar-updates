from socketIO_client import SocketIO, LoggingNamespace
from mailshake import ToFileMailer, SMTPMailer
import requests
import click
from threading import Thread
from tempfile import mkdtemp
import os
from . import printer
from . import emailer



def print_arrival_slip(url):
    url = url_for('.arrival_slip', dewar_name=dewar_name, _external=True)


def get_dewar_data(api_url, name):
    dewars_url = ('{base_url}/dewars/{dewar}'
                  .format(base_url=api_url, dewar=name))
    response = requests.get(dewars_url)
    return response.json()['data']


class PuckTrackerMonitor():

    def __init__(self, host, port, api_url, templates_url, mailer):
        self.host = host
        self.port = port
        self.api_url = api_url
        self.templates_url = templates_url
        self.mailer = mailer

    def run(self):
        socketIO = SocketIO(self.host, self.port, LoggingNamespace)
        socketIO.on('action', self.on_action)
        socketIO.wait()

    def on_action(self, action):
        action_type = action.pop('type', None)
        if action_type is None:
            return
        callback = getattr(self, 'on_' + action_type.lower(), None)
        if callback is None:
            return
        callback(**action)

    def on_update_dewar(self, dewar, update, **_):
        if update.get('onsite'):
            arrival_slip_url = ('{base_url}/arrival-slip/{dewar}'
                                .format(base_url=self.templates_url, dewar=dewar))
            dewar_data = get_dewar_data(self.api_url, dewar)
            Thread(target=printer.print_page, args=(arrival_slip_url,)).start()
            Thread(target=emailer.send_arrival_email,
                   args=(dewar_data, self.mailer)).start()
        elif update.get('missing'):
            dewar_data = get_dewar_data(self.api_url, dewar)
            Thread(target=emailer.send_missing_email,
                   args=(dewar_data, self.mailer)).start()

    def on_set_dewar_offsite(self, dewar, **_):
        dewar_data = get_dewar_data(self.api_url, dewar)
        Thread(target=emailer.send_departed_email,
               args=(dewar_data, self.mailer)).start()

    def on_dewar_filled(self, dewar, **_):
        dewar_data = get_dewar_data(self.api_url, dewar)
        Thread(target=emailer.send_filled_email,
               args=(dewar_data, self.mailer)).start()


@click.command()
@click.option('--socket', default='localhost:8010')
@click.option('--api', default='http://localhost:8001')
@click.option('--templates', default='http://localhost:5000')
def main(socket, api, templates):
    assert 'DEWAR_UPDATES_CC' in os.environ
    config = os.environ.get('DEWAR_UPDATES_CONFIG', 'development')
    if config == 'production':
        mailer = SMTPMailer('mail.synchrotron.org.au', use_tls=True)
    else:
        directory = mkdtemp()
        print('Saving emails to', directory)
        mailer = ToFileMailer(directory)
    host, _, port = socket.partition(':')
    port = int(port)
    monitor = PuckTrackerMonitor(host, port, api, templates, mailer)
    monitor.run()


if __name__ == '__main__':
    main()
