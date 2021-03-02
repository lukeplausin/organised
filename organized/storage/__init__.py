from .. import logger
import os

from .base_storage import BaseStorage
from .base_file import BaseFile
from .amazon_s3_storage import AmazonS3Storage, AmazonS3File


def get_storage(path, **kwargs):
    # Dynamically select a storage backend depending on the format
    input_dir = os.path.expanduser(os.path.expandvars(path))
    if input_dir.startswith("s3://"):
        return AmazonS3File(
            storage=AmazonS3Storage(**kwargs),
            path=path
        )
    if input_dir.startswith("od://"):
        raise NotImplementedError("OneDrive storage not implemented yet")
    if input_dir.startswith("gs://"):
        raise NotImplementedError("Google storage not implemented yet")
    if input_dir.startswith("acs://"):
        raise NotImplementedError("Azure cloud storage not implemented yet")
    if input_dir.startswith("gd://"):
        raise NotImplementedError("Google drive not implemented yet")
    else:
        return BaseFile(storage=BaseStorage(), path=input_dir)
