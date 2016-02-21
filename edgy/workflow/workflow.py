# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from edgy.workflow.constants import WILDCARD


class Workflow(object):
    """
    A ``Workflow`` is a coherent set of Transitions meant to define a state machine system.

    """

    @property
    def states(self):
        """
        Set of valid known states for this workflow. Beware, if you're using wildcard as source,
        there can be states you expect as valid that this instance does not know about, and will
        treat as invalid.

        :return: set[str]
        """
        return set(self._valid_states)

    @property
    def transitions(self):
        """
        Set of transitions living in this state machine system.

        :return: set[edgy.workflow.Transition]
        """
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
        """Add a transition to this workflow instance, to be used on stateful subjects later.

        :param edgy.workflow.Transition transition: Transition to add.

        """
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

        return transition

    def get_available_transitions_for(self, subject):
        transitions = self._transitions_by_source.get(subject.state, {})
        transitions.update(self._transitions_by_source.get(WILDCARD, {}))
        return transitions
