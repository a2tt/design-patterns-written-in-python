class Memento:
    """ memento """

    def __init__(self, content: str):
        self.content = content

    def get_content(self) -> str:
        return self.content


class TextEditor:
    """ originator """

    def __init__(self):
        self.history = []
        self.content = ''

    def write(self, text: str):
        self.content += text

    def read(self):
        print(self.content)

    def save(self) -> Memento:
        return Memento(self.content)

    def restore(self, memento: Memento):
        self.content = memento.get_content()


if __name__ == '__main__':
    editor = TextEditor()
    editor.write('The memento pattern')
    editor.read()
    saved = editor.save()

    editor.write(' provides ability to restore an object to its previous state.')
    editor.read()
    editor.restore(saved)

    editor.read()
