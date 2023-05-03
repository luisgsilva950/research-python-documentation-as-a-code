import os
from unittest import TestCase

from src.state_machine import StateMachineTransaction, StateMachine


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

        transitions = [StateMachineTransaction(label='Mov A -> B', source=states[0], destiny=states[1]),
                       StateMachineTransaction(label='Mov B -> C', source=states[1], destiny=states[2]),
                       StateMachineTransaction(label='Loop C', source=states[2], destiny=states[2])]

        machine = StateMachine(title="Test", states=states, transactions=transitions)

        filename = self.__get_file_name()
        machine.save_as_svg(filename=filename)

        directories = list(os.walk('.'))[0][2]

        self.assertEqual(2, len([d for d in directories if filename in d]))
        self.assertTrue(self.__get_file_name() in directories)
        self.assertTrue(self.__get_svg_file_name() in directories)