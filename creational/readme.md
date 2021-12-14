# Creational Pattern

Wikipedia says
> In software engineering, creational design patterns are design patterns 
> that deal with object creation mechanisms, trying to create objects 
> in a manner suitable to the situation.
> The basic form of object creation could result in design problems or in added complexity to the design.
> Creational design patterns solve this problem by somehow controlling this object creation.

-----

| Pattern | Description |
|:-------:| :---------- |
| [Abstract Factory](#Abstract-Factory) | Class containing a group of factory methods that have something in common. |
| [Factory Method](#Factory-Method) |  |
| [Abstract factory vs Factory Method](#Abstract-factory-vs-Factory-Method) | |
| [Builder](#Builder) |  |
| [Singleton](#Singleton) |  |
| [Multiton](#Multiton) |  |
| [Prototype](#Prototype) |  |
| [RAII](#RAII) |  |

-----

Abstract Factory
----------------

**Wikipedia says**
> The abstract factory pattern provides a way to encapsulate a group of
> individual factories that have a common theme without specifying
> their concrete classes.  
> This pattern provides an interface for creating families of related or
> dependent objects without specifying their concrete classes.

**In my words**
> Class containing a group of factory methods that have something in common. 

**Example**
> To create UI system with various types, we defined RawUI and TailwindUI classes.
> Each classes has its own theme and has several elements, which have a unique rendering method.

```python
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
```
`Element` is the concrete class that we want to create.
The `RawElement` and `TailwindElement` will render differently each other.  

```python
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
```
The `UI` is an abstract factory class that is to create `Element`s.
We have `RawUI` and `TailwindUI`. They have their own theme since they create distinct `Element`s.

```python
class UIRenderer:
    """ Client class that uses abstract class to instantiate concrete classes """

    def __init__(self, ui: UI):
        self.ui = ui

    def render(self):
        header = self.ui.create_header()
        div = self.ui.create_div()

        print(header.render('headerrrr'))
        print(div.render('divvvv')) 
```
As you can see, the `UIRenderer`, a client, creates elements calling the interfaces of the ui variable.
The object creation is delegated to the `UI` abstract factory instead of created by the client directly.

**Related**
- [Factory Method](#Factory-Method)
- [Abstract factory vs Factory Method](#Abstract-factory-vs-Factory-Method)

Factory Method
----------------

Abstract factory vs Factory Method
----------------

Builder
----------------

Singleton
----------------

Multiton
----------------

Prototype
----------------

RAII
----------------
