from abc import ABC, abstractmethod


class Article:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class News(Article):
    pass


class Post(Article):
    pass


class Crawler(ABC):
    @classmethod
    def crawl(cls):
        # do crawling
        page_content = ''  # crawled contents
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


class NewsCrawler(Crawler):
    @classmethod
    def _parse_page(cls, page_content) -> Article:
        # parse page_content
        return News(title='', content='')


class BlogCrawler(Crawler):
    @classmethod
    def _parse_page(cls, page_content) -> Article:
        # parse page_content
        return Post(title='', content='')


if __name__ == '__main__':
    news = NewsCrawler.crawl()
    post = BlogCrawler.crawl()
