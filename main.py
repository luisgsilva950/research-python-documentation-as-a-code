from src.state_machine import StateMachine, StateMachineTransition


def example_state_machine():
    states = ['Home', 'Wait', 'Opponent Seek', 'Move Forward', 'Move Back']

    transitions = [StateMachineTransition(label='Turn On', source=states[0], destiny=states[1]),
                   StateMachineTransition(label='5s', source=states[1], destiny=states[1]),
                   StateMachineTransition(label='T > 5s', source=states[1], destiny=states[2]),
                   StateMachineTransition(label='Opponent not found', source=states[2], destiny=states[2]),
                   StateMachineTransition(label='Opponent found', source=states[2], destiny=states[3]),
                   StateMachineTransition(label='Edge not found', source=states[3], destiny=states[3]),
                   StateMachineTransition(label='Edge found', source=states[3], destiny=states[4]),
                   StateMachineTransition(label='100ms', source=states[4], destiny=states[4]),
                   StateMachineTransition(label='T > 100ms', source=states[4], destiny=states[2])]
    return StateMachine(title="Simple Sumo Robot", states=states, transitions=[*transitions])


if __name__ == '__main__':
    sm = example_state_machine()
    sm.save_as_svg('state_machine_sumo_robot_simple')
