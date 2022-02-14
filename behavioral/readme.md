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
| [State](#-State) | Alter object's behavior when its internal state changes.  |
| [Strategy](#-Strategy) | Allow to select an algorithm based on the situation at runtime. |
| [State vs Strategy](#State-vs-Strategy) | |
| [Template Method](#-Template-Method) | Defines the skeleton of an overall steps while allowing subclasses to implement the steps. |
| [Visitor](#-Visitor) | Define a separate object that implements an operation to be performed on elements of an object structure. |

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


🦎 State
---------

**Wikipedia says**
> The state pattern allows an object to alter its behavior when its internal state changes. This pattern is close to the concept of finite-state machines. The state pattern can be interpreted as a strategy pattern, which is able to switch a strategy through invocations of methods defined in the pattern's interface.

**In my words**
> Alter object's behavior when its internal state changes. 

**Example**
> Imagine a simple text editor. When it is in a `NewSentenceState`, the state object sets `UpperCaseState` as new editor's state to write the first character in upper case, and then sets `LowerCaseState` to write the rest in lower case.

```python
class State(ABC):
    @abstractmethod
    def write(self, editor: TextEditor, text: str):
        raise NotImplementedError


class DefaultState(State):
    def write(self, editor: TextEditor, text: str):
        editor.content += text


class LowerCaseState(State):
    def write(self, editor: TextEditor, text: str):
        editor.content += text.lower()


class UpperCaseState(State):
    def write(self, editor: TextEditor, text: str):
        editor.content += text.upper()


class NewSentenceState(State):
    def write(self, editor: TextEditor, text: str):
        editor.set_state(UpperCaseState())
        editor.write_text(text[0])

        editor.set_state(LowerCaseState())
        editor.write_text(text[1:])
```

```python
class TextEditor:
    def __init__(self):
        self.state = DefaultState()
        self.content = ''

    def set_state(self, state: State):
        self.state = state

    def write_text(self, text: str):
        self.state.write(self, text)
```

```plaintext
>>> editor = TextEditor()
>>> editor.set_state(NewSentenceState())
>>> editor.write_text('hi, I\'m a2tt. ')

>>> editor.set_state(NewSentenceState())
>>> editor.write_text('the `a2tt` is a base64 encoded string of my initials.')
>>> print(editor.content)
Hi, i'm a2tt. The `a2tt` is a base64 encoded string of my initials.
```

**Related**
- [Strategy](#-Strategy)
- [State vs Strategy](#State-vs-Strategy)
- Dependency Injection


🥷 Strategy
---------

**Wikipedia says**
> The strategy pattern enables selecting an algorithm at runtime. Instead of implementing a single algorithm directly, code receives run-time instructions as to which in a family of algorithms to use.

**In my words**
> Allow to select an algorithm based on the situation at runtime.

**Example**
> When you search an integer in a list, you have several options for which algorithm to use. If there are two options, sequential search and binary search, you will use the former for the unsorted list, and the latter for the sorted one.

```python
class Strategy(ABC):
    @abstractmethod
    def find_idx(self, items, target: int) -> int:
        raise NotImplementedError


class SequentialStrategy(Strategy):
    def find_idx(self, items, target: int) -> int:
        for idx, item in enumerate(items):
            if item == target:
                return idx
        return -1


class BinarySearchStrategy(Strategy):
    def find_idx(self, items, target: int) -> int:
        idx = bisect.bisect_left(items, target)
        if idx != len(items) and items[idx] == target:
            return idx
        return -1


class Searcher:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def find_idx(self, items: List[int], target: int) -> int:
        print(f'Find {target} from {items} using {self.strategy.__class__.__name__}')
        return self.strategy.find_idx(items, target)
```

```plaintext
>>> tests = [
>>>     [1, 7, 4, 9, 10, -1, -3, 2],
>>>     [-3, -1, 1, 2, 4, 7, 9, 10]
>>> ]

>>> sequential_strategy = SequentialStrategy()
>>> binary_strategy = BinarySearchStrategy()
>>> searcher = Searcher(sequential_strategy)

>>> for items in tests:
>>>     strategy = binary_strategy if sorted(items) == items else sequential_strategy
>>>     searcher.set_strategy(strategy)
>>>     print(searcher.find_idx(items, 2))
Find 2 from [1, 7, 4, 9, 10, -1, -3, 2] using SequentialStrategy
7
Find 2 from [-3, -1, 1, 2, 4, 7, 9, 10] using BinarySearchStrategy
3
```
Now, the `Searcher` object chooses an algorithm dynamically depending on the state of the list.

**A.K.A.**
- Policy

**Related**
- [State](#-State)
- [State vs Strategy](#State-vs-Strategy)
- Dependency Injection


State vs Strategy
-----------------

**State**
- It is about **doing different things** based on the state.
- The state object is allowed to replace itself to another state.

**Strategy**
- It is about having **different implementation that accomplishes the same thing**.
- It is not allowed to replace strategy object itself to another one.


🖼️ Template Method
--------------------------

**Wikipedia says**
> The template method is a method in a super class, usually an abstract superclass, and defines the skeleton of an operation in terms of a number of high-level steps. These steps are themselves implemented by additional helper methods in the same class as the template method.  
> The intent of the template method is to define the overall structure of the operation, while allowing subclasses to refine, or redefine, certain steps.

**In my words**
> Defines the skeleton of an overall steps while allowing subclasses to implement the steps.

**Example**
> Imagine a website crawler. It visits a webpage, gather data from the page and save the data to somewhere. These three steps are a general pattern of a crawler. Executing these steps is encapsulated in a template method by a superclass, and each step is implemented by subclasses.

```python
class Crawler(ABC):
    def __init__(self, url: str):
        self.url = url
        self.crawled = []

    def start(self):
        """
        The Skeleton of crawler's operations.
        This method is not allowed to be overridden.
        """
        self.fetch_page()
        self.parse()
        self.save()

    @abstractmethod
    def fetch_page(self):
        raise NotImplementedError

    @abstractmethod
    def parse(self):
        raise NotImplementedError

    def save(self):
        print(f'Save {len(self.crawled)} articles to database')


class TwitterCrawler(Crawler):
    def fetch_page(self):
        print('Fetch twitter page', self.url)

    def parse(self):
        print('Parse twitter page')


class RedditCrawler(Crawler):
    def fetch_page(self):
        print('Fetch reddit page', self.url)

    def parse(self):
        print('Parse reddit page')
```

```plaintext
>>> TwitterCrawler('https://twitter.com').start()
Fetch twitter page https://twitter.com
Parse twitter page
Save 0 articles to database

>>> RedditCrawler('https://reddit.com').start()
Fetch reddit page https://reddit.com
Parse reddit page
Save 0 articles to database
```


🏃 visitor
--------------------------

**Wikipedia says**
> The visitor design pattern is a way of separating an algorithm from an object structure on which it operates. A practical result of this separation is the ability to add new operations to existing object structures without modifying the structures.  
> In essence, the visitor allows adding new virtual functions to a family of classes, without modifying the classes. Instead, a visitor class is created that implements all of the appropriate specializations of the virtual function. The visitor takes the instance reference as input, and implements the goal through double dispatch.

**In my words**
> Define a separate object that implements an operation to be performed on elements of an object structure.

**Example**
```python
class Element(ABC):
    def __init__(self):
        self.children: List[Element] = []

    @abstractmethod
    def accept(self, visitor: Visitor):
        for child in self.children:
            child.accept(visitor)

    def add_child(self, element: Element):
        self.children.append(element)


class A(Element):
    def accept(self, visitor: Visitor):
        super().accept(visitor)
        visitor.visit_a(self)


class B(Element):
    def accept(self, visitor: Visitor):
        super().accept(visitor)
        visitor.visit_b(self)
```

```python
class Visitor(ABC):
    @abstractmethod
    def visit_a(self, element: Element):
        raise NotImplementedError

    @abstractmethod
    def visit_b(self, element: Element):
        raise NotImplementedError


class PrintVisitor(Visitor):
    def visit_a(self, element: Element):
        print('Visit A', element)

    def visit_b(self, element: Element):
        print('Visit B', element)


class LogVisitor(Visitor):
    def visit_a(self, element: Element):
        print('Log A', element)

    def visit_b(self, element: Element):
        print('Log B', element)
```

```plaintext
>>> a = A()
>>> a.accept(PrintVisitor())
Visit A <__main__.A object at 0x7f093e8aad10>

>>> a.accept(LogVisitor())
Log A <__main__.A object at 0x7f093e8aad10>

>>> b = B()
>>> b.add_child(a)
>>> b.accept(PrintVisitor())
Visit A <__main__.A object at 0x7f093e8aad10>
Visit B <__main__.B object at 0x7f093e8aa8f0>

>>> b.accept(LogVisitor())
Log A <__main__.A object at 0x7f093e8aad10>
Log B <__main__.B object at 0x7f093e8aa8f0>
```
