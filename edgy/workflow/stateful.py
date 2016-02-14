# -*- coding: utf-8 -*-

import functools


class StatefulObject(object):
    workflow = None
    initial_state = None
    current_state = None

    def __new__(cls, *args, **kwargs):
        if not cls.workflow:
            raise RuntimeError('It is not possible to instanciate a StatefulObject without a workflow.')
        state = kwargs.pop('state', None)
        instance = super(StatefulObject, cls).__new__(cls)
        if state:
            instance.current_state = state
        return instance


    def __repr__(self):
        print(self.state, self.workflow.states)
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

    state = property(fget=_get_state, fset=_set_state)
