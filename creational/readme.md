# Creational Pattern

**Wikipedia says**
> In software engineering, creational design patterns are design patterns 
> that deal with object creation mechanisms, trying to create objects 
> in a manner suitable to the situation.
> The basic form of object creation could result in design problems or in added complexity to the design.
> Creational design patterns solve this problem by somehow controlling this object creation.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Abstract Factory](#-Abstract-Factory) | Class containing a group of factory methods that have something in common. |
| [Factory Method](#-Factory-Method) | Subclasses decide which class to instantiate. |
| [Abstract factory vs Factory Method](#Abstract-factory-vs-Factory-Method) |  |
| [Builder](#-Builder) | Construct a complex object step by step using a builder object. |
| [Singleton](#-Singleton) | Ensure that a class only has one instance and define a public access point to it. |
| [Multiton](#-Multiton) | Mapped singleton instances |
| [Prototype](#-Prototype) | Clone the prototype to produce new objects |

-----

🏭 Abstract Factory
----------------

**Wikipedia says**
> The abstract factory pattern provides a way to encapsulate a group of
> individual factories that have a common theme without specifying
> their concrete classes.  
> This pattern provides an interface for creating families of related or
> dependent objects without specifying their concrete classes.

**In my words**
> Class containing a group of factory methods that have something in common. 

**Example**
> To create UI system with various types, we defined `RawUI` and `TailwindUI` classes.
> Each classes has its own theme and has several elements, which have a unique rendering method.

```python
class Element(ABC):
    """ Concrete class """

    def __init__(self, style: str, tag: str = ''):
        self.style = style
        self.tag = tag

    @abstractmethod
    def render(self, content: str) -> str:
        raise NotImplementedError


class RawElement(Element):
    def render(self, content: str):
        return f'{content}'


class TailwindElement(Element):
    def render(self, content: str):
        return f'<{self.tag} class="{self.style}">{content}</{self.tag}>'
```
`Element` is the concrete class we want to create.
The `RawElement` and `TailwindElement` will render differently each other.  

```python
class UI(ABC):
    """ Abstract factory class """
    STYLE = 'Normal'

    @abstractmethod
    def create_header(self) -> Element:
        raise NotImplementedError

    @abstractmethod
    def create_div(self) -> Element:
        raise NotImplementedError


class RawUI(UI):
    def create_header(self) -> Element:
        return RawElement(self.STYLE)

    def create_div(self) -> Element:
        return RawElement(self.STYLE)


class TailwindUI(UI):
    STYLE = 'TailwindUI'

    def create_header(self) -> Element:
        return TailwindElement(self.STYLE, 'h1')

    def create_div(self) -> Element:
        return TailwindElement(self.STYLE, 'div')
```
The `UI` is an abstract factory class that is to create `Element`s.
We have `RawUI` and `TailwindUI`. They have their own theme since they create distinct `Element`s.

```python
class UIRenderer:
    """ Client class that uses abstract factory class to instantiate concrete classes """

    def __init__(self, ui: UI):
        self.ui = ui

    def render(self):
        header = self.ui.create_header()
        div = self.ui.create_div()

        print(header.render('headerrrr'))
        print(div.render('divvvv')) 
```
As you can see, the `UIRenderer`, a client, creates elements calling the interfaces of the ui variable.
The object instantiation is delegated to the `UI` abstract factory instead of the client doing it directly.

**Related**
- [Factory Method](#-Factory-Method)
- [Abstract Factory vs Factory Method](#Abstract-Factory-vs-Factory-Method)

🏗 Factory Method
----------------

**Wikipedia says**
> In class-baed programming, the factory method pattern is a creational pattern that uses 
> factory methods to deal with the problem of creating objects without having to specify
> the exact class of the object that will be created. This is done by creating objects
> by calling a factory method rather than by calling a constructor.

**In my words**
> Subclasses decide which class to instantiate. 

**Example**
> We build two kind of crawler to parse web page and to return `Article` object.
> Both of them is supposed to parse title and content, and especially `NewsCrawler` 
> to parse the date published.

```python
class Article:
    """ Concrete class """

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def __repr__(self):
        return f'{self.title} - {self.content[:50]}'


class News(Article):
    def __init__(self, title: str, content: str, published_at: str):
        super().__init__(title, content)
        self.published_at = published_at

    def __repr__(self):
        return f'{self.published_at} | ' + super().__repr__()
```
`Article` is the concrete class we want to instantiate and `News` inherits from it.

```python
class Crawler(ABC):
    """ class containing factory method """

    @classmethod
    def crawl(cls) -> Article:
        # do crawling ...
        page_content = ''  # crawled web content
        article = cls._parse_page(page_content)
        return article

    @classmethod
    @abstractmethod
    def _parse_page(cls, page_content) -> Article:
        """
        subclasses override this factory method
        to parse page differently and to return different object
        """
        raise NotImplementedError


class BlogCrawler(Crawler):
    @classmethod
    def _parse_page(cls, page_content) -> Article:
        # parse page_content
        title = 'Article title'
        content = 'Article content'
        return Article(title=title, content=content)


class NewsCrawler(Crawler):
    @classmethod
    def _parse_page(cls, page_content) -> News:
        # parse page_content
        title = 'News title'
        content = 'News content'
        published_at = '2021-12-15'
        return News(title=title, content=content, published_at=published_at)
```
`Crawler` abstract class have an interface, `_parse_page`, which is supposed to parse the page
and to return `Article` or `News` object depending on the subclass it implements.  
Creating object is delegated to the factory method so we don't need to specify what exact class to instantiate
but implement subclasses of the `Crawler` class.

**Related**
- [Abstract Factory](#-Abstract-Factory)
- [Abstract Factory vs Factory Method](#Abstract-Factory-vs-Factory-Method)

Abstract Factory vs Factory Method
----------------

- Both of the patterns decouple the creation of objects from the implementation of them.  
- **Abstract Factory** is an object. **Factory Method** is a method.
- **Abstract Factory** can have several factory methods that instantiate a group 
of different classes of common theme.  
- Because **Factory Method** is a method, subclasses can override the method to create different object. 

**Abstract Factory**

```python
""" `Foo` and `Bar` have something in common in that they are Metasyntactic variable. """
class Foo: pass
class Bar: pass

class SpecialFoo(Foo): pass
class SpecialBar(Bar): pass

class Factory:
    """ Abstract Factory """
    def create_foo(self):
        return Foo()
    def create_bar(self):
        return Bar()

class SpecialFactory(Factory):
    def create_foo(self):
        return SpecialFoo()
    def create_bar(self):
        return SpecialBar()

class Client:
    def do_something(self, factory: Factory):
        f = factory.create_foo()
        b = factory.create_bar()
        # do something with f, b
```

**Factory Method**

```python
class Foo: pass
class FooB(Foo): pass

class A:
    def create_foo(self):
        """ factory method """
        return Foo()

class B(A):
    def create_foo(self):
        """ factory method """
        return FooB()
```

🧱 Builder
----------------

**Wikipedia says**
> The builder pattern is a design pattern designed to provide a flexible solution to various
> object creation problems in object-oriented programming. The intent of the Builder design pattern
> is to separate the construction of a complex object from its representation. 

**In my words**
> Construct a complex object step by step using a builder object.

**Example**
> Imagine you made a push system. Each push has information like user id, landing url, message and so on.  
> You noticed setting the attributes are more complex than you thought.
> So you decided to make a push builder class to separate the 'construction' of the push from its usage.

```python
class PushNotification:
    def __init__(self, user: Union[int, str], url: str, content: str,
                 extra: dict = None):
        self.user = user
        self.url = url
        self.content = content
        self.extra = extra

    def __repr__(self):
        return f'To {self.user}\nURL: {self.url}\n{self.content}'


class PushBuilder:
    def __init__(self):
        self.user = None
        self.content = None
        self.url = None
        self.extra = {}

    def set_user(self, user: Union[int, str]):
        self.user = user

    def set_content(self, content: str):
        self.content = content

    def set_url(self, url: str):
        self.url = url

    def set_extra(self, extra: dict):
        if type(extra) == dict:
            self.extra.update(extra)
            self.extra = extra

    def build(self) -> PushNotification:
        return PushNotification(self.user, self.url, self.content, self.extra)
```
The `PushBuilder` class has several methods that set attributes for the `PushNotification`.
You can set each attributes step by step calling the setter methods.
When you call `PushBuilder.build`, the builder instantiates `PushNotification` class with the set attributes.   

🤴 Singleton
----------------

**Wikipedia says**
> In software engineering, the singleton pattern is a software design pattern that restricts
> the instantiation of a class to one "single" instance.

**In my words**
> Ensure that a class only has one instance and define a public access point to it.

**Example**
> Consider a logger object that write log messages to a file.
> Because the logger writes to a file, in some cases it would be better to have globally one logger
> to prevent unexpected problems concerning the writing.

```python
class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """ Instantiate the singleton class if not created yet and return the object. """
        with cls._lock:  # Prevent simultaneous instantiation in a multi threaded environment.
            if not cls._instance:
                cls._instance = object.__new__(cls)

        return cls._instance

    def log(self, *args):
        print(*args)
```
You can get a logger object by calling `Logger()` and as a singleton, only one of the `Logger` object
can be instantiated per process.

Because the sole object is kept alive throughout the process and a client is tightly coupled with the object,
it would be more difficult to test them. 

**Related**
- [Multiton](#-Multiton)
- Lazy Loading

👪 Multiton
----------------

**Wikipedia says**
> In software engineering, the multiton pattern is a design pattern which generalizes the singleton pattern.
> Whereas the singleton allows only one instance of a class to be created, the multiton pattern allows for the 
> controlled creation of multiple instances, which it manages through the use of a map.

**In my words**
> Mapped singleton instances

**Example**
> Suppose your application connects several types of database and you want to keep establishing only one connection to each database.

```python
class DataBase:
    REGISTRY = {}

    def __new__(cls, type_):
        """
        Instantiate the multiton class when `type_` has never been used to
        created and return the object.
        """
        # Thread-safe operations required (ex. lock)
        if type_ not in cls.REGISTRY.keys():
            cls.REGISTRY[type_] = object.__new__(cls)

        return cls.REGISTRY[type_]
```

The multiton pattern has same disadvantages with the singleton pattern. Tight coupling could happen and 
it would become more difficult to test relevant classes. 

**A.K.A.**
- Registry
- Registry of singletons

**Related**
- [Singleton](#-Singleton)
- [Flyweight vs Multiton](../structural/readme.md#Flyweight-vs-Multiton)
- Lazy Loading

🦎 Prototype
----------------

**Wikipedia says**
> It is used when the type of objects to create is determined by a prototypical instance, which is cloned to 
> produce new objects. This pattern is used to avoid subclasses of an object creator in the client application and 
> to avoid the inherent cost of creating a new object in the standard way.

**In my words**
> Clone the prototype to produce new objects

**Example**
> Imagine a class that requires 100 seconds to instantiate because there are many expensive steps.
> If there is no change of reducing the initialization time and you should absolutely use the prohibitively
> expensive object, then you can use prototype pattern. 

```python
class Prototype:
    def __init__(self, name):
        self.name = name
        # there might be more expensive processes to initialize object

    def clone(self, name=None) -> Prototype:
        _clone = copy.deepcopy(self)  # or
        if name:
            _clone.name = name
        return _clone
```

Yet some other languages provide built-in `clone` functions, in Python, you can use `copy.deepcopy` to clone object.   
