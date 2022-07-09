import configparser
import logging as log
import os

from flask import Flask

CONFIG_FILE = 'src/resources/config.ini'


def configure_logger(level=log.INFO):
    log.basicConfig()
    log.getLogger().setLevel(level)


def load_environment():
    os.environ['PUZZLE_SOLVER_CONFIG_FILE'] = CONFIG_FILE
    if not os.path.exists(CONFIG_FILE):
        log.error(f'{CONFIG_FILE} does not exist')
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    log.debug(config.items())
    if 'general' not in config:
        log.error('Config file is not properly configured')
    return config


def create_app():
    # Load app modules locally to ensure that the configuration and environment variables are set up
    from api.controllers import grid_game_controller

    app = Flask(__name__)

    app.register_blueprint(grid_game_controller)

    return app


if __name__ == '__main__':
    config = load_environment()
    debug = False
    log_level = config['general'].getint('log_level')
    if log_level == log.DEBUG:
        debug = True

    configure_logger(log_level)

    log.info("Start Server...")
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=debug)
