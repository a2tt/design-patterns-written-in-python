from abc import ABC, abstractmethod


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


def main():
    post = BlogCrawler.crawl()
    news = NewsCrawler.crawl()

    print(post)
    print(news)


if __name__ == '__main__':
    main()
