class AWSS3:
    @staticmethod
    def get_object():
        print('This is AWS S3 object')


class AzureBlob:
    @staticmethod
    def get_blob():
        print('This is Azure blob')


class FileSystem:
    @staticmethod
    def get_file():
        print('This is local file')


class AWSS3ToFileSystemAdapter(AWSS3):
    """ class adapter """

    def get_file(self):
        return self.get_object()


class FileSystemAdapter:
    """ object adapter """

    def __init__(self, fs):
        self.fs = fs

    def get_file(self):
        if type(self.fs) == AWSS3:
            return self.fs.get_object()
        elif type(self.fs) == AzureBlob:
            return self.fs.get_blob()
        elif type(self.fs) == FileSystem:
            return self.fs.get_file()


if __name__ == '__main__':
    AWSS3ToFileSystemAdapter().get_file()

    FileSystemAdapter(AWSS3()).get_file()
    FileSystemAdapter(AzureBlob()).get_file()
    FileSystemAdapter(FileSystem()).get_file()
