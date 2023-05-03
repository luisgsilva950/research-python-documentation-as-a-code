from enum import Enum
from typing import List

import graphviz
from transitions import Machine

from src.diagram import Diagram


class StateMachineDirection(Enum):
    TOP_TO_BOTTOM = 'TB'
    BOTTOM_TO_TOP = 'BT'
    LEFT_TO_RIGHT = 'LR'
    RIGHT_TO_LEFT = 'RL'


class GraphColors(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    PURPLE = 'purple'
    CYAN = 'cyan'
    MAGENTA = 'magenta'
    GRAY = 'gray'
    BLACK = 'black'
    WHITE = 'white'
    LIGHT_RED = 'lightred'
    LIGHT_GREEN = 'lightgreen'
    LIGHT_BLUE = 'lightblue'
    LIGHT_YELLOW = 'lightyellow'
    LIGHT_ORANGE = 'lightorange'
    LIGHT_PURPLE = 'lightpurple'
    LIGHT_CYAN = 'lightcyan'
    LIGHT_MAGENTA = 'lightmagenta'
    LIGHT_GRAY = 'lightgray'


class StateMachineTransaction:

    def __init__(self, source: str, destiny: str, label: str):
        self.label = label
        self.source = source
        self.destiny = destiny

    def to_machine_dict(self):
        return dict(trigger=self.label, source=self.source, dest=self.destiny)


class StateMachine(Diagram):
    def __init__(self, title: str, states: List[str], transactions: List[StateMachineTransaction],
                 direction: StateMachineDirection = StateMachineDirection.TOP_TO_BOTTOM,
                 box_color=GraphColors.LIGHT_GRAY):
        self.title = title
        self.direction = direction
        self.box_color = box_color
        self.machine = Machine(model=self, states=[*states], transitions=[t.to_machine_dict() for t in transactions],
                               initial=states[0], auto_transitions=False)
        self.graph = graphviz.Digraph(format='svg',
                                      graph_attr={'ranksep': '0.5', 'nodesep': '0.5', 'rankdir': self.direction.value},
                                      node_attr={'style': 'filled', 'fillcolor': self.box_color.value, 'shape': 'egg'},
                                      edge_attr={})

    def save_as_svg(self, filename: str):
        self.graph.attr(label=self.title, labelloc='t', fontsize='20')

        for state in self.machine.states:
            self.graph.node(state)

        for trigger, transition in self.machine.events.items():
            for t_label, transitions in transition.transitions.items():
                for t in transitions:
                    self.graph.edge(t.source, t.dest, label="  {}  ".format(trigger))

        self.graph.render(filename)
