from typing import List, TypeVar, Optional, Generic

T = TypeVar('T')


class Tag(Generic[T]):
    def __init__(self, raw_text=''):
        self.children: List[Optional[T]] = []
        self.raw_text = raw_text

    def append(self, el: Optional[T]):
        self.children.append(el)

    def render(self, depth: int = 0):
        self._print_open_tag(depth)
        for child in self.children:
            child: Tag
            child.render(depth + 1)
        self._print_close_tag(depth)

    def _print_open_tag(self, depth: int):
        print('\t' * depth, f'<{type(self).__name__.lower()}>')

    def _print_close_tag(self, depth: int):
        print('\t' * depth, f'</{type(self).__name__.lower()}>')


class Div(Tag):
    pass


class UL(Tag):
    pass


class LI(Tag):
    def render(self, depth: int = 0):
        self._print_open_tag(depth)
        print('\t' * (depth + 1), f'{self.raw_text}')
        self._print_close_tag(depth)


if __name__ == '__main__':
    root_div = Div()
    ul_1 = UL()
    ul_2 = UL()

    li_1 = LI('li 1')
    li_2 = LI('li 2')
    li_3 = LI('li 3')

    root_div.append(ul_1)
    root_div.append(ul_2)

    ul_1.append(li_1)
    ul_1.append(li_2)
    ul_2.append(li_3)

    root_div.render()
