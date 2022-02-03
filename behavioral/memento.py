from typing import List

class Memento:
    """ memento """

    def __init__(self, content: str):
        self.content = content

    def get_content(self) -> str:
        return self.content


class TextEditor:
    """ originator """

    def __init__(self):
        self.history: List[Memento] = []
        self.history_limit = 3
        self.content = ''

    def write(self, text: str):
        self.save()
        self.content += text

    def read(self):
        print(self.content)

    def save(self) -> Memento:
        self.history.append(Memento(self.content))

        if len(self.history) > self.history_limit:
            self.history = self.history[-1 * self.history_limit:]

    def rollback(self, step: int = -1):
        try:
            memento = self.history[step]
            self.history = self.history[:step]
            self.content = memento.get_content()
        except IndexError:
            pass


if __name__ == '__main__':
    editor = TextEditor()

    editor.write('The memento pattern')
    editor.write(' provides ability')
    editor.write(' to restore an object')
    editor.write(' to its previous state.')
    editor.read()

    editor.rollback(-3)  # "The memento pattern"
    editor.read()
