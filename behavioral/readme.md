# Behavioral  Pattern

**Wikipedia says**
> In software engineering, behavioral design patterns are design patterns that identify 
> common communication patterns among objects. By doing so, these patterns increase 
> flexibility in carrying out communication.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Chain-of-Responsibility](#-Chain-of-Responsibility) | Define a chain of the request handler objects each having its responsibility. |
| [Command](#-Command) | Encapsulate all information needed to perform an action as an object. |
| [Iterator](#-Iterator) | Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation. |
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




📦 Command
--------------------------

**Wikipedia says**
> The command pattern is a behavioral design pattern in which an object is used to encapsulate all information needed to perform an action or trigger an event at a later time. This information includes the method name, the object that owns the method and values for the method parameters.

**In my words**
> Encapsulate all information needed to perform an action as an object. 
> It mirrors the semantics of first-class functions and higher-order functions

**Example**

```python
class Bulb:
    """ Receiver """

    @staticmethod
    def turn_on():
        print('Let there be light.')

    @staticmethod
    def turn_off():
        print('Let there be darkness.')
```

```python
class Command(ABC):
    """ Command interface class """

    def __init__(self, bulb: Bulb):
        self.bulb = bulb

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class TurnOnCommand(Command):
    def execute(self):
        self.bulb.turn_on()


class TurnOffCommand(Command):
    def execute(self):
        self.bulb.turn_off()

```

```python
class Button:
    """ Invoker class """

    @staticmethod
    def press(command: Command):
        command.execute()
```


```python
>>> # receiver
>>> bulb = Bulb()

>>> # command
>>> turn_on_command = TurnOnCommand(bulb)
>>> turn_off_command = TurnOffCommand(bulb)

>>> # invoker
>>> button = Button()

>>> button.press(turn_on_command)
Let there be light.

>>> button.press(turn_off_command)
Let there be darkness.
```


♾️ Interpreter
--------------------------

**Wikipedia says**
> The iterator pattern is a design pattern in which an iterator is used to traverse a container and
> access the container's elements. The iterator pattern decouples algorithms from containers.

**In my words**
> Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

**Example**

Python itself already implements the iterator pattern as a generator.

```python
def counter(start: int, end: int):
    """ Built-in generator """

    for c in range(start, end + 1):
        yield c
```
```
>>> for c in counter(6, 8):
>>>     print(c)
6
7
8
```
you can implement a generator function like this. 
The function returns a lazy iterator. Whenever you iterate it, it starts to run the code from the previously stopped position(ex. yield), and returns a value.

Or, make a custom one.

```python
class Counter:
    """ Custom iterator """

    def __init__(self, start: int, end: int):
        self.num = start - 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.num < self.end:
            self.num += 1
            return self.num

        raise StopIteration
```
```
>>> for c in Counter(2, 4):
>>>    print(c)
2
3
4
```
Clients of the iterator can traverse the iterable object, but does not need to know its representation.


**A.K.A**
- Cursor