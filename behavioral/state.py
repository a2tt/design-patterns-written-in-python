""" Such a cliche example. """
from __future__ import annotations
from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def write(self, editor: TextEditor, text: str):
        raise NotImplementedError


class DefaultState(State):
    def write(self, editor: TextEditor, text: str):
        editor.content += text


class LowerCaseState(State):
    def write(self, editor: TextEditor, text: str):
        editor.content += text.lower()


class UpperCaseState(State):
    def write(self, editor: TextEditor, text: str):
        editor.content += text.upper()


class NewParagraphState(State):
    def write(self, editor: TextEditor, text: str):
        editor.state = UpperCaseState()
        editor.write_text(text[0])

        editor.state = LowerCaseState()
        editor.write_text(text[1:])


class TextEditor:
    def __init__(self):
        self.state = DefaultState()
        self.content = ''

    def set_state(self, state: State):
        self.state = state

    def write_text(self, text: str):
        self.state.write(self, text)


def main():
    editor = TextEditor()
    editor.write_text('Hi, I\'m a2tt.\n')

    editor.set_state(NewParagraphState())
    editor.write_text('the `a2tt` is a base64 encoded string of the initial of my name.')

    print(editor.content)


if __name__ == '__main__':
    main()
