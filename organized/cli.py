import click
import logging

from . import logger, log_handler
from .organize import main, ORGANIZER_NAMES


@click.group()
@click.option('--debug/--no-debug', default=False)
def organize(debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
        log_handler.setLevel(logging.DEBUG)
        logger.debug('Debug mode is ON.')


from .helpers.camera_organizer import DEFAULT_BASE_PATH, DEFAULT_EXTENSIONS, DEFAULT_FILE_PATH
@organize.command(help='Organize photograph files based on data in the exif tags.')
@click.argument('input-dir')
# @click.option(
#     '--organizers', multiple=True, show_default=True,
#     help=f'Which organizers to run?'
# )
@click.option(
    '--dry-run/--no-dry-run', default=False, show_default=True,
    help='If specified, does nothing but explains what would change.')
@click.option(
    '--prompt/--no-prompt', default=True, show_default=True,
    help='If specified, ask user for confirmation before doing anything.')
@click.option(
    '--base-path', default=DEFAULT_BASE_PATH, show_default=True,
    help='Where should I send the photos to?')
@click.option(
    '--file-path', default=DEFAULT_FILE_PATH, show_default=True,
    help='''What should I save the photos as?
    Use the exif tags as in the python format function.
    ''')
def camera(input_dir, **kwargs):
    main(organizers=['camera'], input_dir=input_dir, **kwargs)


from .helpers.junkfile_organizer import JUNK_FILENAMES, JUNK_EXTENSIONS
@organize.command(help='Organize files and directories according to your preferences')
@click.argument('input-dir')
@click.option(
    '--dry-run/--no-dry-run', default=False, show_default=True,
    help='If specified, does nothing but explains what would change.')
@click.option(
    '--prompt/--no-prompt', default=True, show_default=True,
    help='If specified, ask user for confirmation before doing anything.')
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
