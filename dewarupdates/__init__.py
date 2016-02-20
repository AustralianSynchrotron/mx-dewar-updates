from flask import Flask
from flask.ext.qrcode import QRcode
from flask.ext.bootstrap import Bootstrap
from .config import config


__version__ = '0.3.2'


qr_code = QRcode()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    qr_code.init_app(app)
    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
