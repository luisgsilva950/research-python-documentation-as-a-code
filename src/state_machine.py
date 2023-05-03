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
    LIGHT_RED = 'lightcoral'
    LIGHT_GREEN = 'lightgreen'
    LIGHT_BLUE = 'lightblue2'
    LIGHT_YELLOW = 'lightyellow'
    LIGHT_ORANGE = 'lightorange'
    LIGHT_PURPLE = 'lightslateblue'
    LIGHT_CYAN = 'lightcyan'
    LIGHT_MAGENTA = 'lightcoral'
    LIGHT_GRAY = 'lightgray'


class StateMachineTransition:

    def __init__(self, source: str, destiny: str, label: str):
        self.label = label
        self.source = source
        self.destiny = destiny

    def to_machine_dict(self):
        return dict(trigger=self.label, source=self.source, dest=self.destiny)


class StateMachine(Diagram):
    def __init__(self, title: str, states: List[str], transitions: List[StateMachineTransition] = None,
                 direction: StateMachineDirection = StateMachineDirection.TOP_TO_BOTTOM,
                 box_color=GraphColors.LIGHT_GRAY):
        self.title = title
        self.direction = direction
        self.box_color = box_color
        self.states = states
        self.transitions = transitions or []
        self.machine = None
        self.update_machine()
        self.graph = graphviz.Digraph(format='svg',
                                      graph_attr={'ranksep': '0.5', 'nodesep': '0.5', 'rankdir': self.direction.value},
                                      node_attr={'style': 'filled', 'fillcolor': self.box_color.value, 'shape': 'egg'},
                                      edge_attr={})

    def update_machine(self):
        self.machine = Machine(model=self, states=[*self.states],
                               transitions=[t.to_machine_dict() for t in self.transitions],
                               initial=self.states[0], auto_transitions=False)

    def add_transition(self, transition: StateMachineTransition):
        if transition.source not in self.states:
            self.states = [*self.states, transition.source]
        if transition.destiny not in self.states:
            self.states = [*self.states, transition.destiny]
        self.transitions.append(transition)
        self.update_machine()

    def save_as_svg(self, filename: str):
        self.graph.attr(label=self.title, labelloc='t', fontsize='20')

        for state in self.machine.states:
            self.graph.node(state)

        for trigger, transition in self.machine.events.items():
            for t_label, transitions in transition.transitions.items():
                for t in transitions:
                    self.graph.edge(t.source, t.dest, label="  {}  ".format(trigger))

        self.graph.render(filename)
