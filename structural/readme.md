# Structural Pattern

**Wikipedia says**
> In software engineering, structural design patterns are design patterns that ease the design
> by identifying a simple way to realize relationships among entities.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Adapter](#Adapter) | Wrapper converting the incompatible class into compatible one. |
| [Bridge](#Bridge) |  |
| [Composite](#Composite) |  |
| [Decorator](#Decorator) |  |
| [Facade](#Facade) |  |
| [Flyweight](#Flyweight) |  |
| [Flyweight vs Multiton](#Flyweight-vs-Multiton) |  |
| [Marker](#Marker) |  |
| [Twin](#Twin) |  |
| [Proxy](#Proxy) |  |
| [Decorator vs Proxy](#Decorator-vs-Proxy) |  |

-----

🔌 Adapter
----------------

**Wikipedia says**
> In software engineering, the adapter pattern is a software design pattern that allows the interface of
> an existing class to be used as another interface. It is often used to make existing classes work with others
> without modifying their source code.

**In my words**
> Wrapper converting the incompatible class into compatible one.

**Example**
> Consider that you have made three types of file storage classes, AWSS3, AzureBlob and FileSystem.
> Now you need to make AWSS3 compatible with FileSystem class but they implement different interfaces.
> In this case you can use adapter pattern for AWSS3 interface to be used like FileSystem one.

```python
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
```
The `AWSS3ToFileSystemAdapter` is an adapter class that make `AWSS3` compatible with `FileSystem`,
so the `get_file` interface of `FileSystem` could be used for `AWSS3`.

```python
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
```
Instead of creating a class adapter, an object adapter could be used. `FileSystemAdapter` contains
`fs` object as a variable, and calls method of `fs` depending on its class.

**A.K.A.**
- Translator
- Wrapper

** Related**
- [Decorator](#Decorator) : Dynamically adds responsibility to the interface by wrapping the original code.
- [Facade](#Facade) : Provides a simplified interface.
