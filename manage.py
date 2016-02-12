#!/usr/bin/env python3

from flask.ext.script import Manager
from dewarupdates import create_app
import os


if __name__ == '__main__':
    app = create_app(os.environ.get('DEWAR_UPDATES_CONFIG', 'development'))
    manager = Manager(app)
    manager.run()
