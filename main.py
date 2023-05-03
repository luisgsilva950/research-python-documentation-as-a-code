from src.state_machine import StateMachine, StateMachineTransaction


def example_state_machine():
    states = ['Inicial', 'Espera', 'Procura Oponente', 'Move Frente', 'Move Ré']

    transitions = [StateMachineTransaction(label='Liga', source=states[0], destiny=states[1]),
                   StateMachineTransaction(label='5s', source=states[1], destiny=states[1]),
                   StateMachineTransaction(label='T > 5s', source=states[1], destiny=states[2]),
                   StateMachineTransaction(label='Oponente não encontrado', source=states[2], destiny=states[2]),
                   StateMachineTransaction(label='Oponente encontrado', source=states[2], destiny=states[3]),
                   StateMachineTransaction(label='Borda não encontrada', source=states[3], destiny=states[3]),
                   StateMachineTransaction(label='Borda encontrada', source=states[3], destiny=states[4]),
                   StateMachineTransaction(label='100ms', source=states[4], destiny=states[4]),
                   StateMachineTransaction(label='T > 100ms', source=states[4], destiny=states[2])]

    return StateMachine(title="Simple Sumo Robot", states=states, transactions=transitions)


if __name__ == '__main__':
    sm = example_state_machine()
    sm.save_as_svg('state_machine_sumo_robot_simple')
