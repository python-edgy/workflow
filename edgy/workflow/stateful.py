# -*- coding: utf-8 -*-
"""
For now, a "stateful object" is, to this library, anything that as a "state" attribute that can
be read. If it quacks, then it's a duck.

However, as an helper class to demonstrate how a workflow can be bound to an object, we provide
``StatefulObject`` as an example implementation that you can use.

"""

from __future__ import absolute_import, print_function, unicode_literals

import functools


class StatefulObject(object):
    """
    Example stateful object.

    To use it, subclass me and set the workflow attribute to a ``edgy.workflow.Workflow`` instance.

    .. attribute:: workflow

        A workflow instance, setting the system in which the instances of this object live.

    .. attribute:: initial_state

        The default initial state of this object.

    .. attribute:: current_state

        The current state of this object.

    """
    workflow = None
    initial_state = None
    current_state = None

    @property
    def available_transitions(self):
        return self.workflow.get_available_transitions_for(self)

    def __new__(cls, *args, **kwargs):
        if not cls.workflow:
            raise RuntimeError(
                'It is not possible to instanciate a StatefulObject without a workflow.')
        state = kwargs.pop('state', None)
        instance = super(StatefulObject, cls).__new__(cls)
        if state:
            instance.current_state = state
        return instance

    def __repr__(self):
        return '<{}.{} object with {} "{}" at {}>'.format(
            type(self).__module__,
            type(self).__name__,
            'state' if self.state in self.workflow.states else 'unknown state',
            self.state,
            hex(id(self)),
        )

    def __getattr__(self, attr):
        if attr in self.workflow:
            return functools.partial(self.workflow[attr], subject=self)

        raise AttributeError("%r object has no attribute %r" % (self.__class__, attr))

    def _get_state(self):
        return self.current_state or self.initial_state

    def _set_state(self, state):
        self.current_state = state

    state = property(fget=_get_state, fset=_set_state, doc='''
    Helper for getting the actual state of an object. You should use this instead of
    ``initial_state`` and ``current_state`` if your only aim is to read or write a new state to
    this object.

    Beware though, the setter of this property will override the state, without going through the
    transitions. If you wanna run the transitions (and in 95% of the cases, you should, otherwise
    this library is a pretty bad choice for you), then a proxy attribute exist on the object
    for each transition name, and you should just call it (for example, if a transition is named
    ``wakeup``, you can just call ``instance.wakeup()``).
    ''')
