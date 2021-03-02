import click
import logging

from . import logger, log_handler
from .organize import main, ORGANIZER_NAMES
from .storage.amazon_s3_storage import AWS_CLI_PARAMETERS

@click.group()
@click.option('--debug/--no-debug', default=False)
def organize(debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
        log_handler.setLevel(logging.DEBUG)
        logger.debug('Debug mode is ON.')

GENERIC_CLI_PARAMETERS = [
    click.Option(
        ['--dry-run/--no-dry-run'], required=False, default=False,
        show_default=True,
        help='If specified, does nothing but explains what would change.'
    ),
    click.Option(
        ['--prompt/--no-prompt'], required=False, default=True,
        show_default=True,
        help='If specified, ask user for confirmation before doing anything.'
    ),
]

ALL_CLI_PARAMETERS = GENERIC_CLI_PARAMETERS + AWS_CLI_PARAMETERS

print(AWS_CLI_PARAMETERS)
def _add_click_parameters(params, **kwargs):
    """
    Given a list of click parameter objects,
    attach them in the decorator to the click command.
    """
    def decorator(f):
        # Add in reverse order
        for idx in range(len(params)-1, -1, -1):
            param = params[idx]
            click.decorators._param_memo(f, param)
        return f
    return decorator


from .helpers.camera_organizer import DEFAULT_BASE_PATH, DEFAULT_EXTENSIONS, DEFAULT_FILE_PATH
@organize.command(help='Organize photograph files based on data in the exif tags.')
@click.argument('input-dir')
# @click.option(
#     '--organizers', multiple=True, show_default=True,
#     help=f'Which organizers to run?'
# )
@click.option(
    '--base-path', default=DEFAULT_BASE_PATH, show_default=True,
    help='Where should I send the photos to?')
@click.option(
    '--file-path', default=DEFAULT_FILE_PATH, show_default=True,
    help='''What should I save the photos as?
    Use the exif tags as in the python format function.
    ''')
# Add generic options
@_add_click_parameters(ALL_CLI_PARAMETERS)
def camera(input_dir, **kwargs):
    main(organizers=['camera'], input_dir=input_dir, **kwargs)


from .helpers.junkfile_organizer import JUNK_FILENAMES, JUNK_EXTENSIONS
@organize.command(help='Organize files and directories according to your preferences')
@click.argument('input-dir')
@click.option(
    '--cleanup-empty-dirs/--no-cleanup-empty-dirs', default=True, show_default=True,
    help='If specified, deletes empty directories.')
@click.option(
    '--junk-filenames', default=JUNK_FILENAMES, show_default=True,
    help='Any files matching these filenames will be deleted.')
@click.option(
    '--junk-extensions', default=JUNK_EXTENSIONS, show_default=True,
    help='Any files with these filename extensions will be deleted.')
def dejunk(input_dir, **kwargs):
    main(organizers=['junk'], input_dir=input_dir, **kwargs)
