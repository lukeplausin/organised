import os
import shutil
import subprocess
import logging


logger = logging.getLogger(__name__)


from . import BaseOrganiser


class GitOrganiser(BaseOrganiser):
    def __init__(self, config):
        self.config = config
        self.file_list = []
        self.dir_list = []

        self.directories = ['.git']
        self.files = ['.gitignore', '.gitattributes', '.mailmap', '.gitmodules', '.keep']

    def match_file(self, path):
        if os.path.basename(path) in self.files:
            self.file_list.append(path)
            return True
        else:
            return False

    def match_dir(self, path):
        if os.path.isdir(os.path.join(path, '.git')):
            self.dir_list.append(path)
            return True
        else:
            return False

    def cleanup_dir(self, path):
        for root, dirs, files in os.walk(path):
            for directory in dirs:
                if directory in self.directories:
                    directory_full = os.path.join(root, directory)
                    logger.info('Removing git directory {}'.format(directory_full))
                    # shutil.rmtree(directory_full)
            for filename in files:
                if filename in self.files:
                    file_full = os.path.join(root, filename)
                    logger.info('Removing git file {}'.format(file_full))
                    # os.remove(file_full)
    
    def cleanup_file(self, path):
        pass

    def process(self, path):
        print('I found a git repository at this file path:\n\t{}'.format(path))
        answer = input('Would you like me to make it smaller by running git clean? [y/n]')
        if answer.lower() == 'y':
            # git_args = ["git", "-C", path, "status"]
            git_args = ["git", "-C", path, "gc", "--aggressive", "--auto"]
            answer = input('Would you also like me to prune commits older than 2 weeks? [y/n]')
            if answer.lower() == 'y':
                git_args.append('--prune')
            # subprocess.call(git_args)
            print(git_args)
            return True
        elif input('Would you like me to remove the git repository all together? (delete .git etc) [y/n]'
        ).lower() == 'y':
            print('cleanup {}'.format(path))
            # self.cleanup(path)
            return True
        else:
            return False

