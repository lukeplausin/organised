from .. import logger

from .base_organizer import BaseOrganizer
from .camera_organizer import CameraOrganizer
from .git_organizer import GitOrganizer
from .junkfile_organizer import JunkOrganizer

all = (
    BaseOrganizer,
    CameraOrganizer,
    GitOrganizer,
    JunkOrganizer
)
