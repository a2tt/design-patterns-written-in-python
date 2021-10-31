from abc import ABC, abstractmethod


class Crawler(ABC):
    """ Crawler and CrawlerEngine is decoupled. """

    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    def crawl_page(self):
        raise NotImplementedError


class GoogleCrawler(Crawler):
    def crawl_page(self):
        self.engine.crawl()
        print('crawl google page')


class TwitterCrawler(Crawler):
    def crawl_page(self):
        self.engine.crawl()
        print('crawl twitter page')


class CrawlerEngine(ABC):
    """ CrawlerEngine object is injected into Crawler. """

    @abstractmethod
    def crawl(self):
        raise NotImplementedError


class ImageCrawlerEngine(CrawlerEngine):
    def crawl(self):
        print('parse image')


class ArticleCrawlerEngine(CrawlerEngine):
    def crawl(self):
        print('parse article')


if __name__ == '__main__':
    crawlers = [
        GoogleCrawler(ImageCrawlerEngine()),
        TwitterCrawler(ArticleCrawlerEngine()),
    ]

    for c in crawlers:
        c.crawl_page()
