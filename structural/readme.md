# Structural Pattern

**Wikipedia says**
> In software engineering, structural design patterns are design patterns that ease the design
> by identifying a simple way to realize relationships among entities.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Adapter](#Adapter) | Wrapper converting the incompatible class into compatible one. |
| [Bridge](#Bridge) | Separate abstraction from its implementation by putting them in separate classes. |
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
