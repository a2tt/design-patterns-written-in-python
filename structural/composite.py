from __future__ import annotations
from typing import List


class TagComponent:
    """  Component class, the abstraction of Composite and Leaf """

    def __init__(self, tag: str, raw_text=''):
        self.tag = tag
        self.raw_text = raw_text

    def render(self, depth: int):
        raise NotImplementedError

    def _print_depth(self, depth: int):
        print('  ' * depth, end='')

    def _print_open_tag(self, depth: int):
        self._print_depth(depth)
        print(f'<{self.tag.lower()}>')

    def _print_close_tag(self, depth: int):
        self._print_depth(depth)
        print(f'</{self.tag.lower()}>')


class Composite(TagComponent):
    """ Composite class, having children """

    def __init__(self, tag: str, raw_text=''):
        super().__init__(tag, raw_text)
        self.children: List[TagComponent] = []

    def append(self, el: TagComponent):
        self.children.append(el)

    def render(self, depth: int = 0):
        self._print_open_tag(depth)
        if self.raw_text:
            self._print_depth(depth + 1)
            print(self.raw_text)
        for child in self.children:
            child.render(depth + 1)
        self._print_close_tag(depth)


class Leaf(TagComponent):
    """ Leaf class, implementing all components methods """

    def render(self, depth: int = 0):
        self._print_open_tag(depth)
        self._print_depth(depth + 1)
        print(self.raw_text)
        self._print_close_tag(depth)


def main():
    root_div = Composite('div')
    ul_1 = Composite('ul')
    ul_2 = Composite('ul')

    li_1 = Leaf('li', 'li 1')
    li_2 = Leaf('li', 'li 2')
    li_3 = Leaf('li', 'li 3')

    root_div.append(ul_1)
    root_div.append(ul_2)

    ul_1.append(li_1)
    ul_1.append(li_2)
    ul_2.append(li_3)

    root_div.render()

    composite_alone = Composite('p')
    composite_alone.render()

    composite_alone.raw_text = 'text in UL'
    composite_alone.render()


if __name__ == '__main__':
    main()
