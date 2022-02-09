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
| [Mediator](#-Mediator) | Controls communications among multiple objects. So the objects won't interact with each other directly, and don't need to know each other. |
| [Memento](#-Memento) | Provides the ability to restore an object to its previous state. |
| [Observer](#-Observer) | When a subject changes its state, all registered observers are notified. |
| [State](#-State) | |
| [Strategy](#-Strategy) | |
| [State vs Strategy](#State-vs-Strategy) | |
| [Template Method](#-Template-Method) | |
| [Visitor](#-Visitor) | |

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


♾️ Iterator
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


🌐 Mediator
----------

**Wikipedia says**
> The mediator pattern defines an object that encapsulates how a set of objects interact. This pattern is considered to be a behavioral pattern due to the way it can alter the program's running behavior.
> With the mediator pattern, communication between objects is encapsulated within a mediator object. Objects no longer communicate directly with each other, but instead communicate through the mediator. This reduces the dependencies between communicating objects, thereby reducing coupling.

**In my words**
> A mediator controls communications among multiple objects. 
> So the objects won't interact with each other directly, and don't need to know each other.

**Example**
> Imagine you are building a system trading. There are a control panel that controls all the system,
> a trader that makes or cancels an order, and an order manager that traces the statuses of the orders.
> Whenever the trader makes an order, it must pass the information about the order to the control panel and the order manager. Instead of sending the message directly, it sends it to the mediator, 
> and then the mediator distributes the message to the specified targets. 

```python
class Mediator:
    """ Mediator """

    def __init__(self):
        self.components: DefaultDict[str, List[Component]] = defaultdict(list)

    def register_component(self, name: str, comp: Component):
        self.components[name].append(comp)

    def event_handler(self, data: dict):
        for target in self.components[data.get('target')]:
            target.event_handler(data)
```
`Mediator` has the `components` variable that interact each other through it.

```python
class Component:
    """
    Colleague components
    Components communicate each other through mediator.
    """
    NAME = ''

    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.mediator.register_component(self.NAME, self)

    def send_event(self, data: dict):
        self.mediator.event_handler(data)

    def event_handler(self, data: dict):
        print(f'{self.NAME} got event: {data}')


class ControlPanel(Component):
    """ control panel component """
    NAME = 'ControlPanel'


class Trader(Component):
    """ trader component """
    NAME = 'Trader'


class OrderManager(Component):
    """ order manager component """
    NAME = 'OrderManager'
```
When the component calls its `send_event` method, the data passed is sent to the mediator,
and then the mediator distributes the message to the target components.

```plaintext
>>> # Create mediator and components
>>> mediator = Mediator()
>>> control_panel = ControlPanel(mediator)
>>> trader = Trader(mediator)
>>> order_manager = OrderManager(mediator)

>>> # In real world, all the events will be emitted in a thread of each component
>>> control_panel.send_event({'target': trader.NAME, 'event': 'MOD_VAR', 'value': 1})
Trader got event: {'target': trader.NAME, 'event': 'MOD_VAR', 'value': 1}
>>> trader.send_event({'target': control_panel.NAME, 'event': 'NEW_ORDER', 'order_id': 1234})
ControlPanel got event: {'target': control_panel.NAME, 'event': 'NEW_ORDER', 'order_id': 1234}
>>> trader.send_event({'target': order_manager.NAME, 'event': 'NEW_ORDER', 'order_id': 1234})
OrderManager got event: {'target': order_manager.NAME, 'event': 'NEW_ORDER', 'order_id': 1234}
>>> order_manager.send_event({'target': control_panel.NAME, 'event': 'TX', 'order_id': 1234})
ControlPanel got event: {'target': control_panel.NAME, 'event': 'TX', 'order_id': 1234}
```
Thanks to the mediator, the components don't need to know the implementations of the others, 
but need to simply specify the name of the target component.


🗯️ Memento
----------

**Wikipedia says**
> The memento pattern is a software design pattern that provides the ability to restore an object to its previous state (undo via rollback).  
> The originator is some object that has an internal state. The caretaker first asks the originator for a memento object. Then it does whatever operation it was going to do. To roll back to the state before the operations, it returns the memento object to the originator.

**In my words**
> Provides the ability to restore an object to its previous state.

**Example**
> Imagine a simple text editor. It has basic operations like `write`, `read`, `save` and `rollback` that would be executed when you press `Ctrl + z`. The rolled back contents can be saved as a `Memento` object.

```python
class Memento:
    """ memento """

    def __init__(self, content: str):
        self.content = content

    def get_content(self) -> str:
        return self.content


class TextEditor:
    """ originator """

    def __init__(self):
        self.history: List[Memento] = []
        self.history_limit = 3
        self.content = ''

    def write(self, text: str):
        self.save()
        self.content += text

    def read(self):
        print(self.content)

    def save(self) -> Memento:
        self.history.append(Memento(self.content))

        if len(self.history) > self.history_limit:
            self.history = self.history[-1 * self.history_limit:]

    def rollback(self, step: int = -1):
        try:
            memento = self.history[step]
            self.history = self.history[:step]
            self.content = memento.get_content()
        except IndexError:
            pass
```

```plaintext
>>> editor = TextEditor()

>>> editor.write('The memento pattern')
>>> editor.write(' provides ability')
>>> editor.write(' to restore an object')
>>> editor.write(' to its previous state.')
>>> editor.read()
The memento pattern provides ability to restore an object to its previous state.

>>> editor.rollback(-3)
>>> editor.read()
The memento pattern
```
When you call `write` of the editor, it saves its current content into the new `Memento` object appending it to the `history` object, and concatenates passed text to the current content.  
When `rollback` is called, it retrieves `step` steps before version from the history and overwrites the current content with the previous one.


👂 Observer
--------------------------

**Wikipedia says**
> In the observer pattern, an object, named the subject, maintains a list of its dependents, called observers, and notifies the mautomatically of any state changes, usually by calling one of their method.

**In my words**
> When a subject changes its state, all registered observers are notified.

**Example**
```python
from __future__ import annotations
from typing import List


class Observable:
    """ Observable """

    def __init__(self):
        self.observers: List[Observer] = []

    def subscribe(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify(self, msg: str):
        for observer in self.observers:
            observer.notify(msg)


class Observer:
    """ Observer """

    def __init__(self, name: str):
        self.name = name

    def notify(self, msg: str):
        print(f'{self.name} got {msg}')
```

```plaintext
>>> observer1 = Observer('observer-1')
>>> observer2 = Observer('observer-2')

>>> observable = Observable()
>>> observable.subscribe(observer1)
>>> observable.subscribe(observer2)

>>> observable.notify('meeeessage')
observer-1 got meeeessage
observer-2 got meeeessage
```

**Related**
- [Mediator](#-mediator)
