# -*- coding: utf-8 -*-
from edgy.workflow import StatefulObject, Workflow


class Subject(object):
    is_duck = False
    is_pumpkin = False
    state = 'human'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super(Subject, self).__init__()


class StatefulSubject(Subject, StatefulObject):
    is_duck = False
    is_pumpkin = False
    initial_state = 'human'
    state = StatefulObject.state  # property
    transitions = []
    _workflow = None

    @property
    def workflow(self):
        if not self._workflow:
            self._workflow = Workflow()
            for transition in self.transitions:
                self._workflow.add_transition(transition)
        return self._workflow


class InvalidStateful(StatefulObject):
    workflow = None
