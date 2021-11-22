from __future__ import annotations
from typing import DefaultDict, List
from collections import defaultdict


class Mediator:
    """ Mediator """

    def __init__(self):
        self.components: DefaultDict[str, List[Component]] = defaultdict(list)

    def register_component(self, name: str, comp: Component):
        self.components[name].append(comp)

    def event_handler(self, data: dict):
        for target in self.components[data.get('target')]:
            target.event_handler(data)


class Component:
    """
    Colleague components
    Components communicate each other through mediator.
    """
    NAME = ''

    def __init__(self, mediator: Mediator):
        self.mediator = mediator
        self.mediator.register_component(self.NAME, self)

    def send_event(self, data: dict):
        self.mediator.event_handler(data)

    def event_handler(self, data: dict):
        print(f'{self.NAME} got event: {data}')


class ControlPanel(Component):
    """ control panel component """
    NAME = 'ControlPanel'


class Trader(Component):
    """ trader component """
    NAME = 'Trader'


class OrderManager(Component):
    """ order manager component """
    NAME = 'OrderManager'


if __name__ == '__main__':
    # Create mediator and components
    mediator = Mediator()
    control_panel = ControlPanel(mediator)
    trader = Trader(mediator)
    order_manager = OrderManager(mediator)

    # In real world, all the events will be emitted in a thread of each component
    control_panel.send_event({'target': trader.NAME, 'event': 'MOD_VAR', 'value': 1})
    trader.send_event({'target': control_panel.NAME, 'event': 'NEW_ORDER', 'order_id': 1234})
    trader.send_event({'target': order_manager.NAME, 'event': 'NEW_ORDER', 'order_id': 1234})
    order_manager.send_event({'target': control_panel.NAME, 'event': 'TX', 'order_id': 1234})
