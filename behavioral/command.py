"""
Failed to think out useful real-world example :@
"""

from abc import ABC, abstractmethod


class Bulb:
    """ Receiver """

    @staticmethod
    def turn_on():
        print('Let there be light.')

    @staticmethod
    def turn_off():
        print('Let there be darkness.')


class Command(ABC):
    """ Command interface class """

    def __init__(self, bulb: Bulb):
        self.bulb = bulb

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class TurnOnCommand(Command):
    def execute(self):
        self.bulb.turn_on()


class TurnOffCommand(Command):
    def execute(self):
        self.bulb.turn_off()


class Button:
    """ Invoker class """

    @staticmethod
    def press(command: Command):
        command.execute()


def main():
    # receiver
    bulb = Bulb()

    # command
    turn_on_command = TurnOnCommand(bulb)
    turn_off_command = TurnOffCommand(bulb)

    # invoker
    button = Button()
    button.press(turn_on_command)
    button.press(turn_off_command)


if __name__ == '__main__':
    main()
