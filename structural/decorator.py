from abc import ABC, abstractmethod


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


if __name__ == '__main__':
    # decorated object
    empty_tag = EmptyTag('test')
    print(empty_tag.get_text())

    # decorator object
    decorated_tag = ItalicTagDecorator(BoldTagDecorator(empty_tag))
    print(decorated_tag.get_text())
