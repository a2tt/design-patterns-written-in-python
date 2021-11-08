from abc import ABC, abstractmethod
from typing import Type


class FileDrive(ABC):
    """ Service """

    @abstractmethod
    def upload(self, file) -> str:
        """ use drive API to upload file """
        raise NotImplementedError


class S3(FileDrive):
    def upload(self, file) -> str:
        return 's3_file_url'


class GoogleDrive(FileDrive):
    def upload(self, file) -> str:
        return 'google_drive_file_url'


class DropBox(FileDrive):
    def upload(self, file) -> str:
        return 'dropbox_file_url'


class FileUploader:
    """ Client which depends on FileDrive(service) """

    def __init__(self, drive: Type[FileDrive] = None):
        self.drive = drive  # construction injection

    def set_file_drive(self, drive: Type[FileDrive]):
        self.drive = drive  # setter injection

    def upload(self, file: object, drive: Type[FileDrive] = None):
        if not self.drive and drive:
            self.drive = drive  # parameter injection

        if not self.drive:
            raise AttributeError('drive is undefined.')

        # FileUploader knows FileDrive interface.
        print(self.drive().upload(file))


if __name__ == '__main__':
    file = object()

    # construction injection
    uploader_1 = FileUploader(S3)
    uploader_1.upload(file)

    # setter injection
    uploader_2 = FileUploader()
    uploader_2.set_file_drive(GoogleDrive)
    uploader_2.upload(file)

    # parameter injection
    uploader_3 = FileUploader()
    uploader_3.upload(file, DropBox)
