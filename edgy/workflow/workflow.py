# -*- coding: utf-8 -*-
from collections import OrderedDict

import six

from edgy.workflow.transition import Transition
from edgy.workflow.constants import WILDCARD


class DeclarativeTransitionsMetaclass(type):
    """
    Metaclass that collects Transitions declared on the base classes.
    """

    def __new__(mcs, name, bases, attrs):
        # Collect transitions from current class.
        current_transitions = []
        for key, value in list(attrs.items()):
            if isinstance(value, Transition):
                current_transitions.append((key, value))
                attrs.pop(key)
        current_transitions.sort(key=lambda x: x[1].creation_counter)
        attrs['declared_transitions'] = OrderedDict(current_transitions)

        new_class = (super(DeclarativeTransitionsMetaclass, mcs).__new__(mcs, name, bases, attrs))

        # Walk through the MRO.
        declared_transitions = OrderedDict()
        for base in reversed(new_class.__mro__):
            # Collect transitions from base class.
            if hasattr(base, 'declared_transitions'):
                declared_transitions.update(base.declared_transitions)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in declared_transitions:
                    declared_transitions.pop(attr)

        new_class.declared_transitions = declared_transitions

        return new_class


class Workflow(six.with_metaclass(DeclarativeTransitionsMetaclass)):
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
        self._transitions = OrderedDict()
        self._transitions_by_source = {}
        self._valid_states = {WILDCARD}

        for name, transition in self.declared_transitions.items():
            self.add_transition(transition, name=name)

    def __contains__(self, item):
        return item in self._transitions

    def __getitem__(self, item):
        return self._transitions[item]

    def add_transition(self, transition, name=None):
        """Add a transition to this workflow instance, to be used on stateful subjects later.

        :param edgy.workflow.Transition transition: Transition to add.

        """
        name = name or transition.__name__

        # store the transition by name
        self._transitions[name] = transition

        # ensure we know source and target states as valid
        self._valid_states = self._valid_states.union(set(transition.source))
        self._valid_states.add(transition.target)

        # index transitions by source state
        for source_state in transition.source:
            if not source_state in self._transitions_by_source:
                self._transitions_by_source[source_state] = {}
            self._transitions_by_source[source_state][name] = transition

        return transition

    def get_available_transitions_for(self, subject):
        transitions = self._transitions_by_source.get(subject.state, {})
        transitions.update(self._transitions_by_source.get(WILDCARD, {}))
        return transitions

