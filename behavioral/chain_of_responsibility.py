from __future__ import annotations

import os
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Optional

File = namedtuple('File', ['source'])


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
        print('Searching from GoogleDrive')
        file = False  # ex) find = google_drive.search_file(filepath)
        if not file:
            return self.successor.load_file(filepath) if self.successor else None

        return File('GoogleDrive')


class DropBox(FileLoader):
    BASE_DIR = 'app/data/'

    def load_file(self, filepath: str):
        print('Searching from Dropbox')
        file = False  # ex) find = dropbox.search_file(filepath)
        if not file and self.successor:
            return self.successor.load_file(filepath) if self.successor else None

        return File('Dropbox')


class FileSystem(FileLoader):
    BASE_DIR = os.path.join(os.path.expanduser('~'), 'app')

    def load_file(self, filepath: str):
        print('Searching from local')
        file = filepath if os.path.isfile(os.path.join(self.BASE_DIR, filepath)) else False
        if not file and self.successor:
            return self.successor.load_file(filepath) if self.successor else None

        return File('Local')


class FallbackFileLoader(FileLoader):
    def __init__(self):
        super().__init__(None)

    def load_file(self, filepath: str):
        return


def main():
    """
    Make chain of [GoogleDrive -> DropBox -> FileSystem]
    If the file does not exist in GoogleDrive, then search from DropBox and then from FileSystem. 
    """
    file_loader = FileSystem(GoogleDrive(DropBox(FallbackFileLoader())))
    file = file_loader.load_file('README.md')
    print(file)


if __name__ == '__main__':
    main()
