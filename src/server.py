import logging as log

from flask import Flask

from api.controllers import *


def configure_logger(level=log.INFO):
    log.basicConfig()
    log.getLogger().setLevel(level)


def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_controller)

    return app


if __name__ == '__main__':
    configure_logger(log.DEBUG)

    log.info("Start Server...")
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
    # app.run(host='0.0.0.0', port=5001, debug=True)
