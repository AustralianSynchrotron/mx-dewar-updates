from socketIO_client import SocketIO, LoggingNamespace
import click
from threading import Thread
from . import printer


def print_arrival_slip(url):
    url = url_for('.arrival_slip', dewar_name=dewar_name, _external=True)


class PuckTrackerMonitor():

    def __init__(self, host=None, port=None, templates_url=None):
        self.host = host
        self.port = port
        self.templates_url = templates_url

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
            url = ('{base_url}/arrival-slip/{dewar}'
                   .format(base_url=self.templates_url, dewar=dewar))
            print(url)
            Thread(target=printer.print_page, args=(url,)).start()

    def on_set_dewar_offsite(self, dewar, **_):
        pass

    def on_dewar_filled(self, dewar, **_):
        pass


@click.command()
@click.option('--host', default='localhost')
@click.option('--port', type=int, default=8010)
@click.option('--templates', default='http://localhost:5000')
def main(host, port, templates):
    monitor = PuckTrackerMonitor(host, port, templates)
    monitor.run()


if __name__ == '__main__':
    main()
