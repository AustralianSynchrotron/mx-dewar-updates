#!/usr/bin/env python3

from flask.ext.script import Manager
from dewarupdates import create_app


if __name__ == '__main__':
    app = create_app('development')
    manager = Manager(app)
    manager.run()
