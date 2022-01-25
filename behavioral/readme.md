# Behavioral  Pattern

**Wikipedia says**
> In software engineering, behavioral design patterns are design patterns that identify 
> common communication patterns among objects. By doing so, these patterns increase 
> flexibility in carrying out communication.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Chain-of-Responsibility](#-Chain-of-Responsibility) | Define a chain of the request handler objects each having its responsibility. |
| [Command](#-Command) | |
| [Interpreter](#-Interpreter) | |
| [Iterator](#-Iterator) | |
| [Mediator](#-Mediator) | |
| [Memento](#-Memento) | |
| [Observer](#-Observer) | |
| [State](#-State) | |
| [Strategy](#-Strategy) | |
| [State vs Strategy](#State-vs-Strategy) | |
| [Template Method](#-Template Method) | |
| [Visitor](#-) | |

-----

🖇 Chain of Responsibility
--------------------------

**Wikipedia says**
> The chain-of-responsibility pattern is a behavioral design pattern consisting of a source of command objects
> and a series of processing objects. Each processing object contains logic that defines the types of command objects
> that it can handle; the rest are passed to the next processing object in the chain. 

**In my words**
> Define a chain of the handler objects each having its responsibility. A request proceeds following the chain 
> until it finds the handler that can handle it.

**Example**
> Suppose that you have failed to organize millions of files consistently. Some of them are on your local computer,
> some in Google Drive, and the others in Dropbox. Since you have a list of file names, you decided to do a workaround.
> First, you search from your local computer. If the file you want is not there, you search from Google Drive.
> And then from Dropbox.  

```python
File = namedtuple('File', ['source'])


class FileLoader(ABC):
    def __init__(self, successor: Optional[FileLoader]):
        self.successor: FileLoader = successor

    @abstractmethod
    def load_file(self, filepath: str) -> Optional[File]:
        """ Return file object """
        raise NotImplementedError


class FileSystem(FileLoader):
    BASE_DIR = os.path.join(os.path.expanduser('~'), 'app')

    def load_file(self, filepath: str):
        print('Searching from local')
        file = filepath if os.path.isfile(os.path.join(self.BASE_DIR, filepath)) else False
        if not file and self.successor:
            return self.successor.load_file(filepath)
        if not self.successor:
            return

        return File('Local')

# GoogleDrive and DropBox classes are similar with FileSystem class 


class FallbackFileLoader(FileLoader):
    def __init__(self):
        super().__init__(None)

    def load_file(self, filepath: str):
        return
```
If the `FileLoader` object has a `successor` and fails to find the file, it can call the successor.
And the successor can call its successor, like forming a chain.
Each request handler of the chain has its own responsibility, in this case, searching the specified file.

```text
>>> file_loader = FileSystem(GoogleDrive(DropBox(FallbackFileLoader())))
>>> file = file_loader.load_file('README.md')
>>> print(file)
Searching from local
Searching from GoogleDrive
Searching from Dropbox
None
```
As you can see, the `load_file` methods are executed in order until it finds the file.  
For this reason, the request sender is decoupled with a particular receiver(handler).

 