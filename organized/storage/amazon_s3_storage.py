import boto3
import urllib
import tempfile
import shutil
import os
from .base_storage import BaseStorage
from .base_file import BaseFile
from . import logger


import click
AWS_CLI_PARAMETERS = [
    click.Option(
        ['--aws-profile'], required=False, default=None,
        help='Select an AWS profile to use, if interacting with AWS S3 storage'
    ),
    click.Option(
        ['--aws-region'], required=False, default=None, type=str,
        help='Select an AWS region to use, if interacting with AWS S3 storage'
    ),
]


class AmazonS3Storage(BaseStorage):

    # Class methods
    def split(path):
        if path.startswith('s3://'):
            path_parts = urllib.parse.urlparse(path)
            if not (path_parts.scheme == 's3'):
                raise ValueError(f'Path must be an s3 format URL [s3://mybucket/path/to/file.jpg], received {path}')
            return path_parts.netloc, path_parts.path.lstrip('/')
        else:
            raise ValueError(f'Path must be an s3 format URL [s3://mybucket/path/to/file.jpg], received {path}')

    def __init__(self, **config):
        profile_name = None
        region_name = None
        if 'aws_profile' in config.keys():
            profile_name = config['aws_profile']
        if 'aws_region' in config.keys():
            region_name = config['aws_region']
        self.session = boto3.session.Session(
            profile_name=profile_name, region_name=region_name)

    def is_file(self, path):
        raise NotImplementedError('Not implemented.')
        # return os.path.isfile(path)

    def is_dir(self, path):
        raise NotImplementedError('Not implemented.')
        # return os.path.isdir(path)

    def mkdir(self, path):
        logger.info("Creating directory {}".format(path))
        # return os.makedirs(path)
        raise NotImplementedError('Not implemented.')

    def list_dir(self, path):
        # return os.listdir(path)
        raise NotImplementedError('Not implemented.')

    def rmdir(self, path):
        logger.info("Removing empty directory {}".format(path))
        # return os.rmdir(path)
        raise NotImplementedError('Not implemented.')

    def walk(self, path):
        # Iterate over files and folders
        # return os.walk(path)
        s3 = self.session.client('s3')
        if isinstance(path, AmazonS3File):
            bucket = path.bucket
            bucket_path = path.path
        else:
            bucket, bucket_path = AmazonS3Storage.split(path)
        def yield_dirs():
            pag = s3.get_paginator('list_objects_v2')
            for page in pag.paginate(Bucket=bucket, Prefix=bucket_path, Delimiter='/'):
                for prefix in page.get('CommonPrefixes', []):
                    yield prefix['Prefix']
        def yield_files():
            pag = s3.get_paginator('list_objects_v2')
            for page in pag.paginate(Bucket=bucket, Prefix=bucket_path, Delimiter='/'):
                for object in page.get('Contents', []):
                    yield AmazonS3File(storage=self, bucket=bucket, path=object['Key'], props=object)
        # Yield current directory
        yield (bucket_path, yield_dirs(), yield_files())

        # Recurse
        pag = s3.get_paginator('list_objects_v2')
        for page in pag.paginate(Bucket=bucket, Prefix=bucket_path, Delimiter='/'):
            for prefix in page.get('CommonPrefixes', []):
                full_dir = f"s3://{bucket}/{prefix['Prefix']}"
                # Yield recursively
                yield from self.walk(full_dir)

    def join(self, base, path, as_object=False):
        # Join two file paths
        if base.endswith('/'):
            new_path = base + path
        else:
            new_path = base + '/' + path
        if as_object:
            return self.file(new_path)
        else:
            return new_path

    def file(self, path):
        # Return a new file object from the given path
        return AmazonS3File(storage=self, path=path)


class AmazonS3File(BaseFile):
    def __init__(self, storage=None, bucket=None, path=None, props=None):
        self.storage = storage
        self._local_path = ""
        if bucket and path:
            self.bucket = bucket
            self.path = path
        elif path:
            self.bucket, self.path = AmazonS3Storage.split(path)
        else:
            raise ValueError('Must supply either bucket and path, or path in s3 url format.')
        self.props = props

    def copy(self, destination):
        # Move the file from this path to the destination
        logger.info(f'Copy file {self} to {destination}')
        if isinstance(destination, str):
            dest = destination
        elif destination.__class__ == BaseFile:
            dest = destination.path
        else:
            raise NotImplementedError('Copy to other storage provider not implemented yet.')
        if dest.startswith('s3://'):
            # S3 to S3 copy
            raise NotImplementedError('Not implemented yet sorry')
        else:
            s3 = self.storage.session.client('s3')
            s3.download_file(Bucket=self.bucket, Key=self.path, Filename=dest)

    def local_path(self):
        # Return a file path on the local system where data can be acessed - warning
        # downloads the file to local storage if not currently here.
        if not self._local_path:
            self._local_path = tempfile.mktemp()
            self.copy(self._local_path)
        return self._local_path

    def __str__(self):
        return f's3://{self.bucket}/{self.path}'

    def move(self, destination):
        self.copy(destination)
        self.delete(reason='File moved.')

    def delete(self, reason="(none given)"):
        logger.info("Deleting file {}, reason - {}".format(
            self.path, reason
        ))
        s3 = self.storage.session.client('s3')
        s3.delete_object(Bucket=self.bucket, Key=self.path)
        if self._local_path:
            logger.debug(f'Clean up local copy {self._local_path}')
            os.remove(self._local_path)
            self._local_path = ''
