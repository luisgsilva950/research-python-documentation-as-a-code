import os
from unittest import TestCase
from unittest.mock import Mock

from src.state_machine import StateMachineTransition, StateMachine


class TestStateMachine(TestCase):

    def tearDown(self) -> None:
        try:
            os.remove(self.__get_file_name())
            os.remove(self.__get_svg_file_name())
        except:
            ...

    def __get_file_name(self):
        return f"test_{self.__class__.__name__}_{self._testMethodName}"

    def __get_svg_file_name(self):
        return f"{self.__get_file_name()}.svg"

    def test_should_create_diagram_files(self):
        states = ['A', 'B', 'C']

        transitions = [StateMachineTransition(label='Mov A -> B', source=states[0], destiny=states[1]),
                       StateMachineTransition(label='Mov B -> C', source=states[1], destiny=states[2]),
                       StateMachineTransition(label='Loop C', source=states[2], destiny=states[2])]

        machine = StateMachine(title="Test", states=states, transitions=transitions)

        filename = self.__get_file_name()
        machine.save_as_svg(filename=filename)

        directories = list(os.walk('.'))[0][2]

        self.assertEqual(2, len([d for d in directories if filename in d]))
        self.assertTrue(self.__get_file_name() in directories)
        self.assertTrue(self.__get_svg_file_name() in directories)

    def test_should_call_graph_render_functions(self):
        states = ['A', 'B']

        transitions = [StateMachineTransition(label='A -> B', source=states[0], destiny=states[1]),
                       StateMachineTransition(label='B -> C', source=states[1], destiny=states[1])]

        machine = StateMachine(title="Foobar", states=states, transitions=transitions)
        machine.graph = Mock()
        machine.save_as_svg(filename=self.__get_file_name())
        machine.graph.attr.assert_called_once_with(label="Foobar", labelloc='t', fontsize='20')
        self.assertEqual(2, machine.graph.node.call_count)
        self.assertEqual(2, machine.graph.edge.call_count)
        machine.graph.render.assert_called_once()

    def test_adding_transitions_after(self):
        states = ['A', 'B', 'C']

        transitions = [StateMachineTransition(label='Mov A -> B', source=states[0], destiny=states[1]),
                       StateMachineTransition(label='Mov B -> C', source=states[1], destiny=states[2]),
                       StateMachineTransition(label='Loop C', source=states[2], destiny=states[2])]

        machine = StateMachine(title="Test", states=states)
        machine.add_transition(transitions[0])
        machine.add_transition(transitions[1])
        machine.add_transition(transitions[2])

        machine.graph = Mock()
        machine.save_as_svg(filename=self.__get_file_name())

        machine.graph.attr.assert_called_once_with(label="Test", labelloc='t', fontsize='20')
        self.assertEqual(3, machine.graph.node.call_count)
        self.assertEqual(3, machine.graph.edge.call_count)
        machine.graph.render.assert_called_once()

    def test_adding_transitions_after_with_different_destiny_state(self):
        states = ['A', 'B', 'C']

        transitions = [StateMachineTransition(label='Mov A -> B', source=states[0], destiny=states[1]),
                       StateMachineTransition(label='Mov B -> C', source=states[1], destiny=states[2]),
                       StateMachineTransition(label='Loop C', source=states[2], destiny=states[2])]

        machine = StateMachine(title="Test", states=states)
        machine.add_transition(transitions[0])
        machine.add_transition(transitions[1])
        machine.add_transition(transitions[2])
        machine.add_transition(StateMachineTransition(label='C -> D', source=states[2], destiny='New State'))

        machine.graph = Mock()
        machine.save_as_svg(filename=self.__get_file_name())

        machine.graph.attr.assert_called_once_with(label="Test", labelloc='t', fontsize='20')
        self.assertEqual(4, machine.graph.node.call_count)
        self.assertEqual(4, machine.graph.edge.call_count)
        machine.graph.render.assert_called_once()
