"""
The twin pattern is used in programming languages that do not support
multiple inheritance. Because Python support this feature,
there is no need to use the pattern.
"""

from typing import Optional


class CrawlerEngine:
    """Super-class"""
    NAME = 'base'

    def crawl(self, page: int = 1):
        raise NotImplementedError


class CrawlerController:
    """Super-class"""

    def __init__(self, max_page: int = 3):
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


def main():
    # Multiple inheritance
    RedditCrawler().start()

    # Twin pattern
    starter = CrawlerStarter()
    engine = GoogleCrawlerEngine()

    starter.set_twin(engine)
    engine.set_twin(starter)

    starter.start()


if __name__ == '__main__':
    main()
