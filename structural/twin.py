"""
Twin pattern is used in programming languages that do not support
multiple inheritance. Because Python support this feature, there
is no need to use Twin pattern when other options available.
"""

import time
from typing import Optional


class CrawlerEngine:
    NAME = 'base'

    def __init__(self):
        self.twin: Optional[CrawlerStarter] = None

    def set_twin(self, twin):
        self.twin = twin

    def crawl(self, page: int = 1):
        raise NotImplementedError


class CrawlerStarter:
    def __init__(self):
        self.twin: Optional[CrawlerEngine] = None
        self.counter = 0

    def set_twin(self, twin):
        self.twin = twin

    def incr_crawl_cnt(self):
        self.counter += 1

    def start(self):
        raise NotImplementedError


class GoogleCrawler(CrawlerEngine):
    NAME = 'Google'

    def crawl(self, page: int = 1):
        print(f'Crawling {self.NAME} | page {page}')
        self.twin.incr_crawl_cnt()


class CrawlerPageStarter(CrawlerStarter):
    def start(self):
        page = 1
        while page < 10000 and self.counter < 10:
            self.twin.crawl(page)
            page += 1
            time.sleep(0.05)


if __name__ == '__main__':
    starter = CrawlerPageStarter()
    engine = GoogleCrawler()

    starter.set_twin(engine)
    engine.set_twin(starter)

    starter.start()
