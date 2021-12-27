# Structural Pattern

**Wikipedia says**
> In software engineering, structural design patterns are design patterns that ease the design
> by identifying a simple way to realize relationships among entities.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Adapter](#Adapter) | Wrapper converting the incompatible class into compatible one. |
| [Bridge](#Bridge) | Separate abstraction from its implementation by putting them in separate classes. |
| [Composite](#Composite) | A group of objects are treated the same way as a single instance of the same type of object using tree structure. |
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