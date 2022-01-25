from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Optional



class FileLoader(ABC):
    def __init__(self, successor: Optional[FileLoader]):
        self.successor: FileLoader = successor

    @abstractmethod
    def load_file(self, filepath: str) -> Optional[File]:
        """ Return file object """
        raise NotImplementedError


class GoogleDrive(FileLoader):
    BASE_DIR = 'app/data/'

    def load_file(self, filepath: str):
        file = False  # ex) find = google_drive.search_file(filepath)
        if not file and self.successor:
            return self.successor.load_file(filepath)
        print('found in google drive')
        return file


class DropBox(FileLoader):
    BASE_DIR = 'app/data/'

    def load_file(self, filepath: str):
        file = False  # ex) find = dropbox..search_file(filepath)
        if not file and self.successor:
            return self.successor.load_file(filepath)
        print('found in dropbox')
        return filepath


class FileSystem(FileLoader):
    BASE_DIR = os.path.join(os.path.expanduser('~'), 'app')

    def load_file(self, filepath: str):
        file = filepath if os.path.isfile(os.path.join(self.BASE_DIR, filepath)) else False
        if not file and self.successor:
            return self.successor.load_file(filepath)
        print('found in local file system')
        return file


if __name__ == '__main__':
    """
    Make chain of [GoogleDrive -> DropBox -> FileSystem]
    If the file does not exist in GoogleDrive, then search from DropBox and then from FileSystem. 
    """
    google_drive = GoogleDrive(DropBox(FileSystem()))
    google_drive.load_file('README.md')
