import click
import logging

from . import logger, log_handler


@click.group()
@click.option('--debug/--no-debug', default=False)
def organize(debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
        log_handler.setLevel(logging.DEBUG)
        logger.debug('Debug mode is ON.')
