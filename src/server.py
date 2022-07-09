import argparse
import configparser
import logging as log
import os
import sys

from flask import Flask
from pytesseract import pytesseract
from waitress import serve

CONFIG_DEV_FILE = 'resources/config-dev.ini'
CONFIG_PROD_FILE = 'src/resources/config-prod.ini'


def configure_logger(level=log.INFO):
    log.basicConfig()
    log.getLogger().setLevel(level)


def load_command_line_arguments():
    log.debug('Number of arguments:', len(sys.argv), 'arguments.')
    log.debug('Argument List:', str(sys.argv))

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true", help="run in dev mode")
    parser.add_argument("-p", "--prod", action="store_true", help="run in prod mode")
    args = parser.parse_args()

    if args.dev and args.prod:
        log.warning('Cannot run dev and prod mode simultaneously. Running dev mode instead.')
        args.dev = True
        args.prod = False

    if not args.dev and not args.prod:
        args.dev = True

    return args


def load_environment(args):
    if args.dev:
        config_file = CONFIG_DEV_FILE
    elif args.prod:
        config_file = CONFIG_PROD_FILE
    else:
        raise EnvironmentError('Running mode unknown. Define either dev or prod.')

    os.environ['PUZZLE_SOLVER_CONFIG_FILE'] = config_file
    if not os.path.exists(config_file):
        log.error(f'{config_file} does not exist')
    config = configparser.ConfigParser()
    config.read(config_file)
    log.debug(config.items())
    if 'general' not in config:
        log.error('Config file is not properly configured')
    return config


def load_tesseract(args):
    if args.dev:
        pytesseract.tesseract_cmd = config['tesseract']['executable']  # needed if not running inside docker


def create_app():
    # Load app modules locally to ensure that the configuration and environment variables are set up
    from api.controllers import grid_game_controller

    app = Flask(__name__)

    app.register_blueprint(grid_game_controller)

    return app


if __name__ == '__main__':
    args = load_command_line_arguments()
    config = load_environment(args)
    load_tesseract(args)

    debug = False
    log_level = config['general'].getint('log_level')
    if log_level == log.DEBUG:
        debug = True

    configure_logger(log_level)

    log.info("Start Server...")
    app = create_app()

    ip_address = config['flask']['ip_address']
    port = config['flask'].getint('port')

    if args.prod:
        serve(app, host=ip_address, port=port)
    else:
        app.run(host=ip_address, port=port, debug=debug)
