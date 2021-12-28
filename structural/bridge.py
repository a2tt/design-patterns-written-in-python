from __future__ import annotations
from abc import ABC, abstractmethod


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


def main():
    crawlers = [
        GoogleCrawler(ImageCrawlerEngine()),
        TwitterCrawler(ArticleCrawlerEngine()),
    ]

    for c in crawlers:
        c.crawl_page()


if __name__ == '__main__':
    main()
