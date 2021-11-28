from abc import ABC, abstractmethod


class Crawler(ABC):
    def __init__(self, url: str):
        self.url = url
        self.crawled = []

    def start(self):
        """
        The Skeleton of crawler's operation.
        This methods is not allowed to be overridden.
        """
        self.fetch_page()
        self.parse()
        self.save()

    @abstractmethod
    def fetch_page(self):
        raise NotImplementedError

    @abstractmethod
    def parse(self):
        raise NotImplementedError

    def save(self):
        print(f'Save {len(self.crawled)} articles to database')


class TwitterCrawler(Crawler):
    def fetch_page(self):
        print('Fetch twitter page', self.url)

    def parse(self):
        print('Parse twitter page')


class RedditCrawler(Crawler):
    def fetch_page(self):
        print('Fetch reddit page', self.url)

    def parse(self):
        print('Parse reddit page')


def main():
    TwitterCrawler('https://twitter.com').start()
    RedditCrawler('https://reddit.com').start()


if __name__ == '__main__':
    main()
