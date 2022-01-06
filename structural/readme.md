# Structural Pattern

**Wikipedia says**
> In software engineering, structural design patterns are design patterns that ease the design
> by identifying a simple way to realize relationships among entities.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Adapter](#-Adapter) | Wrapper converting the incompatible class into compatible one. |
| [Bridge](#-Bridge) | Separate abstraction from its implementation by putting them in separate classes. |
| [Composite](#-Composite) | A group of objects are treated the same way as a single instance of the same type of object using tree structure. |
| [Decorator](#-Decorator) | Provide new behavior at run-time for selected objects. |
| [Facade](#-Facade) | A front-facing interface hiding more complex underlying code. |
| [Flyweight](#-Flyweight) | Minimize memory usage by sharing flyweights with other similar objects. |
| [Flyweight vs Multiton](#Flyweight-vs-Multiton) |  |
| [Twin](#-Twin) | Model multiple inheritance in programming languages that do not support it. |
| [Proxy](#-Proxy) |  |
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
- [Decorator](#-Decorator) : Dynamically adds responsibility to the interface by wrapping the original code.
- [Facade](#-Facade) : Provides a simplified interface.

🌉 Bridge
----------------

**Wikipedia says**
> The bridge pattern is a design pattern used in software engineering that is meant to
> "decouple an abstraction from its implementation so that the two can vary independently".
> The bridge uses encapsulation, aggregation, and can use inheritance to separate 
> responsibilities into different classes

**In my words**
> Separate abstraction from its implementation by putting them in separate classes.

**Example**
> Consider you want to build a crawler that crawls Google and Twitter and that parses image and article.
> You can make several crawlers that crawl Google's image, Google's article(post), Twitter's image
> and Twitter's article(tweet) but this is not extensible. You would decide to use bridge pattern.

```python
class Crawler(ABC):
    """ Crawler and CrawlerEngine are decoupled. """

    def __init__(self, engine: CrawlerEngine):
        self.engine = engine

    @abstractmethod
    def crawl_page(self):
        raise NotImplementedError


class GoogleCrawler(Crawler):
    def crawl_page(self):
        print('crawl google page')
        self.engine.crawl()


class TwitterCrawler(Crawler):
    def crawl_page(self):
        print('crawl twitter page')
        self.engine.crawl()


class CrawlerEngine(ABC):
    """ CrawlerEngine object will be injected into Crawler. """

    @abstractmethod
    def crawl(self):
        raise NotImplementedError


class ImageCrawlerEngine(CrawlerEngine):
    def crawl(self):
        print('parse image')


class ArticleCrawlerEngine(CrawlerEngine):
    def crawl(self):
        print('parse article')
```
The `CrawlerEngine` object is injected to the `Crawler` object. 
In this way, you can decouple the abstraction and the implementation of `CrawlerEngine`.

**Related**
- Dependency Injection

🌿 Composite
----------------

**Wikipedia says**
> In software engineering, the composite pattern is a partitioning design pattern.
> The composite pattern describes a group of objects that are treated the same way as a single 
> instance of the same type of object. The intent of a composite is to "compose" objects 
> into tree structures to represent part-whole hierarchies.

**In my words**
> A group of objects are treated the same way as a single instance of the same type of object
> using tree structure.

**Example**
> HTML tags can represent a text and have a collection of child tags inside forming a tree-like structure.
> When the root tag is evaluated, its children are evaluated between the opening/closing tag of the root.
> And it applies to the each child recursively, making it as root tag and evaluating its tree.

```python
class TagComponent:
    """  Component class, the abstraction of Composite and Leaf """

    def __init__(self, tag: str, raw_text=''):
        self.tag = tag
        self.raw_text = raw_text

    def render(self, depth: int):
        raise NotImplementedError

    def _print_depth(self, depth: int):
        print('  ' * depth, end='')

    def _print_open_tag(self, depth: int):
        self._print_depth(depth)
        print(f'<{self.tag.lower()}>')

    def _print_close_tag(self, depth: int):
        self._print_depth(depth)
        print(f'</{self.tag.lower()}>')
```
`Component` class is the abstraction of `Composite` and `Leaf` class.

```python
class Composite(TagComponent):
    """ Composite class, having children """

    def __init__(self, tag: str, raw_text=''):
        super().__init__(tag, raw_text)
        self.children: List[TagComponent] = []

    def append(self, el: TagComponent):
        self.children.append(el)

    def render(self, depth: int = 0):
        self._print_open_tag(depth)
        if self.raw_text:
            self._print_depth(depth + 1)
            print(self.raw_text)
        for child in self.children:
            child.render(depth + 1)
        self._print_close_tag(depth)

```
`Composite` has a special variable `children` to contain any of `Leaf` and `Composite`.

```python
class Leaf(TagComponent):
    """ Leaf class, implementing all components methods """

    def render(self, depth: int = 0):
        self._print_open_tag(depth)
        self._print_depth(depth + 1)
        print(f'{self.raw_text}')
        self._print_close_tag(depth)
```
Iterating from the composite to the children, you can traverse the tree structure.
So the whole hierarchy could be manipulated.

```python
>>> root_div = Composite('div')
>>> ul_1 = Composite('ul')
>>> ul_2 = Composite('ul')

>>> li_1 = Leaf('li', 'li 1')
>>> li_2 = Leaf('li', 'li 2')
>>> li_3 = Leaf('li', 'li 3')

>>> root_div.append(ul_1)
>>> root_div.append(ul_2)

>>> ul_1.append(li_1)
>>> ul_1.append(li_2)
>>> ul_2.append(li_3)

>>> root_div.render()
<div>
  <ul>
    <li>
      li 1
    </li>
    <li>
      li 2
    </li>
  </ul>
  <ul>
    <li>
      li 3
    </li>
  </ul>
</div>
``` 

🎀 Decorator
----------------

**Wikipedia says**
> In object-oriented programming, the decorator pattern is a design pattern that allows behavior to be added 
> to an individual object, dynamically, without affecting the behavior of other objects from the same class.

**In my words**
> Provide new behavior at run-time for selected objects.

**Example**
> Consider you render HTML span tag with different features. Some of them are font-weight, font-family, color
> or something else. Subclasses for each feature could be used, but there will be so many subclasses to cover 
> all combinations of them. Decorator pattern can solve the problem adding each feature through a wrapper 
> not a subclass.

```python
class Tag(ABC):
    """ Decorated class """
    @abstractmethod
    def get_text(self):
        raise NotImplementedError


class EmptyTag(Tag):
    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def get_text(self):
        return self.raw_text
```

```python
class TagDecorator(Tag):
    """ Abstract Decorator class
    It inherits the `Tag` so that the clients can implement it
    as if it is the decorated(`Tag`) object.
    """
    def __init__(self, tag: Tag):
        self.tag = tag  # decorated object

    def get_text(self):
        return self.tag.get_text()


class BoldTagDecorator(TagDecorator):
    def get_text(self):
        return f'<b>{self.tag.get_text()}</b>'


class ItalicTagDecorator(TagDecorator):
    def get_text(self):
        return f'<i>{self.tag.get_text()}</i>'
```

```python
>>> empty_tag = EmptyTag('test')
>>> empty_tag.get_text()
test

>>> decorated_tag = ItalicTagDecorator(BoldTagDecorator(empty_tag))
>>> decorated_tag.get_text()
<i><b>test</b></i>
```
When you implement subclasses for each feature, there are `BoldTag`, `ItalicTag`, `BoldItalicTag`, `RedTag`, `RedBoldTag`, 
`RedItalicBoldTag` and all possible combinations of the features. 
Decorators working as a wrapper do the job preventing unnecessary effort of subclassing.
  

**A.K.A.**
- Wrapper

🚪 Facade
----------------

**Wikipedia says**
> Analogous to a facade in architecture, a facade is an object that serves as a front-facing interface
> masking more complex underlying or structural code. 

**In my words**
> A front-facing interface hiding more complex underlying code.

**Example**
> Do you know Curiosity on Mars? It is NASA's Mars exploration robot. It goes here and there, take a picture,
> take a soil sample and do other things. It is clearly composed of so many parts and
> they operate in a complex way but should operate coordinately.
> A kind of facade method could be used to operate them easily.

```python
class Camera:
    @staticmethod
    def take_a_picture():
        print('take a picture of the view')


class Wheel:
    @staticmethod
    def rotate(deg):
        print(f'rotate {deg}°')

    @staticmethod
    def move():
        print('move forward')


class CuriosityFacade:
    """ https://en.wikipedia.org/wiki/Curiosity_(rover) """

    def __init__(self):
        self.wheel = Wheel()
        self.camera = Camera()

    def move(self, deg: int = 0):
        self.wheel.rotate(deg)
        self.camera.take_a_picture()
        self.wheel.move()
        self.camera.take_a_picture()
```
```
>>> curiosity = CuriosityFacade()
>>> curiosity.move(30)
rotate 30°
take a picture of the view
move forward
take a picture of the view
```

**Related**
- [Adapter](#-Adapter)
- [Decorator](#-Decorator)


🪶 Flyweight
----------------

**Wikipedia says**
> A flyweight refers to an object that minimizes memory usage by sharing some of its data
> with other similar objects.

**In my words**
> Minimize memory usage by sharing flyweights with other similar objects.

**Example**
> Consider there is a badge system in your game and each users has a badge.
> Assumed that the badge has a intrinsic sharable state but not context-dependent one,
> it would be better to instantiate the badge once for each type to reduce memory consumption and for performance.

```python
class Badge:
    """Flyweight"""
    NAME = 'normal'


class VIPBadge(Badge):
    NAME = 'VIP'


class MVPBadge(Badge):
    NAME = 'MVP'


class BadgeFactory:
    _BADGES = {}  # Shared container to the flyweights

    @classmethod
    def get_badge(cls, type_: str) -> Badge:
        if type_ in cls._BADGES:
            return cls._BADGES[type_]

        if type_ == VIPBadge.NAME:
            cls._BADGES[type_] = VIPBadge()
        elif type_ == MVPBadge.NAME:
            cls._BADGES[type_] = MVPBadge()
        else:
            cls._BADGES[type_] = Badge()

        return cls._BADGES[type_]


class User:
    def __init__(self, name: str, badge: str = 'normal'):
        self.name = name
        self.badge = BadgeFactory.get_badge(badge)

    def introduce(self):
        print(f'My name is {self.name} and I have {self.badge.NAME}({id(self.badge)}) badge')
```

```python
>>> for i in range(0, 5):
...     User(str(i), random.choice([Badge.NAME, VIPBadge.NAME, MVPBadge.NAME])).introduce()
...
My name is 0 and I have normal(140171334950704) badge
My name is 1 and I have VIP(140171334950560) badge
My name is 2 and I have MVP(140171334950416) badge
My name is 3 and I have VIP(140171334950560) badge
My name is 4 and I have MVP(140171334950416) badge
```
Even if numerous users have badges, each badge only needs to be instantiated once and they are shared with users.
Therefore, memory consumption and resource could be reduced. 

**Related**
- [Flyweight vs Multiton](#Flyweight-vs-Multiton)
- [Multiton](../creational/readme.md#-Multiton)
- Object Pool


Flyweight vs Multiton
---------------------

**Flyweight**
- Intent: Minimize memory usage by sharing flyweights with other similar objects.
- There is no demand that only a single instance should exist. A class can be instantiate more than once.
- Ex) In word processor, when a character 'A' is a flyweight, then "AAAA" string consists of single 'A' object. 

**Multiton**
- Intent: Ensure that only one instance of a class could be exist for a key. 
- There is a demand that only a single instance per key should exist.


👬 Twin
----------------

**Wikipedia says**
> The twin pattern allows developers to model multiple inheritance. This pattern avoids 
> many of the problems with multiple inheritance.

**In my words**
> Model multiple inheritance in programming languages that do not support it.

The twin pattern is used in programming languages that do not support
multiple inheritance. Because Python support this feature, there is no need to use the pattern.

**Example**
> Consider a crawler consists of a crawler engine and controller. You can implement multiple inheritance of the
> two classes in a single class. But when it is not possible, Twin pattern can be used to workaround this.
> That is, a subclass of the crawler engine has a twin object referencing the crawler controller and 
> a subclass of the crawler controller has a twin object referencing the crawler engine.

```python
class CrawlerEngine:
    """Super-class"""
    NAME = 'base'

    def crawl(self, page: int = 1):
        raise NotImplementedError


class CrawlerController:
    """Super-class"""

    def __init__(self, max_page: int = 5):
        self.max_page = max_page

    def start(self):
        raise NotImplementedError


class RedditCrawler(CrawlerEngine, CrawlerController):
    """Use multiple inheritance"""
    NAME = 'Reddit'

    def crawl(self, page: int = 1):
        print(f'Crawling {self.NAME} | page {page}')

    def start(self):
        page = 1
        while page <= self.max_page:
            self.crawl(page)
            page += 1

        print('Complete')
```
`CrawlerEngine` and `CrawlerController` is the superclasses that we want to implement in a single class and
`RedditCrawler` is an example of multiple inheritance of the classes.  
But what if it is impossible, like in JAVA?

```python
class GoogleCrawlerEngine(CrawlerEngine):
    """Twin sub-class"""
    NAME = 'Google'

    def __init__(self):
        self.twin: Optional[CrawlerController] = None

    def set_twin(self, twin: CrawlerController):
        self.twin = twin

    def crawl(self, page: int = 1):
        print(f'Crawling {self.NAME} | page {page}')


class CrawlerStarter(CrawlerController):
    """Twin sub-class"""

    def __init__(self, max_page: int = 3):
        super().__init__(max_page)
        self.twin: Optional[CrawlerEngine] = None

    def set_twin(self, twin: CrawlerEngine):
        self.twin = twin

    def start(self):
        page = 1
        while page <= self.max_page:
            self.twin.crawl(page)
            page += 1

        print('Complete')
```
`GoogleCrawlerEngine` and `CrawlerStarter` inherits `CrawlerEngine` and `CrawlerController` respectively.  
The point is, they have `self.twin` objects which are set in `set_twin` method and each twin object references
each other.

```text
>>> # Multiple inheritance
>>> RedditCrawler().start()
Crawling Reddit | page 1
Crawling Reddit | page 2
Crawling Reddit | page 3
Complete

>>> # Twin pattern
>>> starter = CrawlerStarter()
>>> engine = GoogleCrawlerEngine()

>>> starter.set_twin(engine)
>>> engine.set_twin(starter)

>>> starter.start()
Crawling Google | page 1
Crawling Google | page 2
Crawling Google | page 3
Complete
```
