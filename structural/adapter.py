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


class AWSS3ToFileSystemAdapter(AWSS3, FileSystem):
    """
    Class Adapter
    This class adapter uses multiple polymorphic interfaces implementing or
    inheriting both the interface that is expected and the interface that
    is pre-existing.
    """

    def get_file(self):
        return self.get_object()


class FileSystemAdapter:
    """
    Object Adapter
    This object adapter contains an instance of the class it wraps and
    makes calls to the instance of the wrapped object.
    """

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
    # Class adapter
    AWSS3ToFileSystemAdapter().get_file()

    # Object adapter
    FileSystemAdapter(AWSS3()).get_file()
    FileSystemAdapter(AzureBlob()).get_file()
    FileSystemAdapter(FileSystem()).get_file()
