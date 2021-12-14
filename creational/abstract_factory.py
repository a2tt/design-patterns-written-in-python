from abc import ABC, abstractmethod


class Element(ABC):
    """ Concrete class """

    def __init__(self, style: str, tag: str = ''):
        self.style = style
        self.tag = tag

    @abstractmethod
    def render(self, content: str) -> str:
        raise NotImplementedError


class RawElement(Element):
    def render(self, content: str):
        return f'{content}'


class TailwindElement(Element):
    def render(self, content: str):
        return f'<{self.tag} class="{self.style}">{content}</{self.tag}>'


class UI(ABC):
    """ Abstract factory class """
    STYLE = 'Normal'

    @abstractmethod
    def create_header(self) -> Element:
        raise NotImplementedError

    @abstractmethod
    def create_div(self) -> Element:
        raise NotImplementedError


class RawUI(UI):
    def create_header(self) -> Element:
        return RawElement(self.STYLE)

    def create_div(self) -> Element:
        return RawElement(self.STYLE)


class TailwindUI(UI):
    STYLE = 'TailwindUI'

    def create_header(self) -> Element:
        return TailwindElement(self.STYLE, 'h1')

    def create_div(self) -> Element:
        return TailwindElement(self.STYLE, 'div')


class UIRenderer:
    """ Client class that uses abstract class to instantiate concrete classes """

    def __init__(self, ui: UI):
        self.ui = ui

    def render(self):
        header = self.ui.create_header()
        div = self.ui.create_div()

        print(header.render('headerrrr'))
        print(div.render('divvvv'))


def main():
    ui_renderer = UIRenderer(RawUI())
    ui_renderer.render()

    ui_renderer = UIRenderer(TailwindUI())
    ui_renderer.render()


if __name__ == '__main__':
    main()
