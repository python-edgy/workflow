# -*- coding: utf-8 -*-

from edgy.workflow.constants import WILDCARD


class Workflow(object):
    @property
    def states(self):
        return set(self._valid_states)

    @property
    def transitions(self):
        return set(self._transitions.items())

    def __init__(self):
        # states and transitions indexes
        self._transitions = {}
        self._transitions_by_source = {}
        self._valid_states = {WILDCARD}

    def __contains__(self, item):
        return item in self._transitions

    def __getitem__(self, item):
        return self._transitions[item]

    def add_transition(self, transition):
        # store the transition by name
        self._transitions[transition.__name__] = transition

        # ensure we know source and target states as valid
        self._valid_states = self._valid_states.union(set(transition.source))
        self._valid_states.add(transition.target)

        # index transitions by source state
        for source_state in transition.source:
            if not source_state in self._transitions_by_source:
                self._transitions_by_source[source_state] = {}
            self._transitions_by_source[source_state][transition.__name__] = transition

    def get_available_transitions_for(self, subject):
        transitions = self._transitions_by_source.get(subject.state, {})
        transitions.update(self._transitions_by_source.get(WILDCARD, {}))
        return transitions
