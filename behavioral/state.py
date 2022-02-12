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


class NewSentenceState(State):
    def write(self, editor: TextEditor, text: str):
        editor.set_state(UpperCaseState())
        editor.write_text(text[0])

        editor.set_state(LowerCaseState())
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
    editor.set_state(NewSentenceState())
    editor.write_text('hi, I\'m a2tt. ')

    editor.set_state(NewSentenceState())
    editor.write_text('the `a2tt` is a base64 encoded string of my initials.')

    print(editor.content)


if __name__ == '__main__':
    main()
