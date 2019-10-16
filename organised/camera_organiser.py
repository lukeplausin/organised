import os
import shutil
import subprocess
import logging
import json
import datetime
import exiftool


logger = logging.getLogger(__name__)


from . import BaseOrganiser, move_file


class CameraOrganiser(BaseOrganiser):
    def __init__(self, config):
        self.config = config
        self.file_list = []
        self.file_extensions = [".jpg", ".jpeg", ".png", ".3gp", ".mov", ".mp4"]
        self.destination = "~/Pictures/MyPhotos/{Date:%Y-%m}_({EXIF_Model})/{Date:%Y%m%d_%H%M%S}.{File_FileTypeExtension}"

        if "org.camera" in self.config["preferences"].keys():
            # Check for overrides in config
            plugin_config = self.config["preferences"]["org.camera"]
            if "file_extensions" in plugin_config.keys():
                self.file_extensions = plugin_config["file_extensions"]
            if "destination" in plugin_config.keys():
                self.destination = plugin_config["destination"]

    def match_file(self, path):
        path_noext, ext = os.path.splitext(path)
        if ext in self.file_extensions:
            judgement = (path, "File has known {} extension".format(ext))
            self.file_list.append(judgement)
            logger.debug("{} match - {}".format(*judgement))
            return True
        else:
            return False
        # else:
        #     for pattern in spec.get('patterns', []):
        #         if re.match(pattern, name):
        #             return True

    def match_dir(self, path):
        return False

    # def match_dir(self, path):
    #     return os.path.isdir(os.path.join(path, '.git'))

    def cleanup_dir(self, path):
        pass
    
    def cleanup_file(self, path):
        pass

    def process(self):
        # Process images with exif metadata
        logger.warning('This function is not implemented yet')
        # with exiftool.ExifTool() as et:
        #     metadata = et.get_metadata_batch(self.file_list)
        
        # for file_metadata in metadata:
        #     try:
        #         # Augment the data
        #         file_metadata = {
        #             k.replace(":", "_"): v for k, v in file_metadata.items()
        #         }
        #         file_metadata['File_FileTypeExtension'] = file_metadata['File_FileTypeExtension'].lower()
        #         if 'EXIF_CreateDate' in file_metadata.keys():
        #             date = file_metadata['EXIF_CreateDate']
        #         else:
        #             date = file_metadata['File_FileModifyDate']
        #         file_metadata['Augmented_CreateDate'] = date
        #         if '+' in date:
        #             date_parsed = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S%z')
        #         else:
        #             date_parsed = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        #         file_metadata['Date'] = date_parsed

        #         # metadata['Augmented:CreateDate'] = date
        #         destination = self.config['camera']['destination'].format(
        #             **file_metadata
        #         )
        #         if (self.config.get('dry_run', True)):
        #             print("DRYRUN: Move file {} to {}".format(
        #                 file_metadata['SourceFile'], destination))
        #         else:
        #             # move_file(file_metadata['SourceFile'], destination)
        #             print("AAAAAARGH!")
                
        #     except KeyError as e:
        #         logger.error("File {} missing key {}".format(file_metadata['SourceFile'], e))
        #         logger.debug(json.dumps(file_metadata, default=str, indent=2))
        #     except Exception as e:
        #         logger.error("Exception: {}".format(e))
