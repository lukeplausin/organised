import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)


DEFAULTS={
    # "input_dir": "~/desktop/"
    "config_dir": "~/.organized/",

    "preferences": {
        "organizers": ["camera", "git", "junk"],
        "org.camera": {
            "file_extensions": [".jpg", ".jpeg", ".png", ".3gp", ".mov", ".mp4"],
            # "destination": "$HOME/Pictures/Camera/{Date:%Y-%b}/{Date:%Y-%m-%d} ({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"
            "destination": "~/Pictures/MyPhotos/{Date:%Y-%m}_({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"
        },
        "org.junk": {
            "file_extensions": [".tmp"],
            "remove_patterns": [".DS_Store"]
        },
        # "movie": {
        #     "extensions": ["mov", "vid", "xvid"]
        # },
        "documents": {
            "extensions": ["doc", "docx", "csv", "txt"]
        }
    }
}
