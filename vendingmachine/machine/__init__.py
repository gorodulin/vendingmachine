# -*- coding: utf-8 -*-

from transitions import Machine as StateMachine
from transitions.extensions.states import add_state_features, Timeout as StateMachineTimeout

@add_state_features(StateMachineTimeout)
class CustomStateMachine(StateMachine): pass

# Note: leave it here
from .machine import Machine
