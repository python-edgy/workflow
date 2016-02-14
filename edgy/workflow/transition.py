# -*- coding: utf-8 -*-

import functools

from edgy.workflow.constants import WILDCARD
from edgy.workflow.utils import issequence


class Transition(object):
    def __new__(cls, handler=None, **kwargs):
        # If we have a complete construction call, let's use default "object" instance creator.
        if handler:
            return super(Transition, cls).__new__(cls)

        # If we're missing a handler, then we return a decorator that will instanciate the transition once a handler has been given.
        @functools.wraps(Transition)
        def decorator(handler):
            return Transition(handler=handler, **kwargs)

        return decorator

    def __init__(self, handler=None, name=None, source=None, target=None):
        self.source = tuple(source if issequence(source) else (source,))
        self.target = target
        self._name = name

        if handler:
            self.handler = handler or self.handler

    def __call__(self, subject, *args, **kwargs):
        if not WILDCARD in self.source and not subject.state in self.source:
            raise RuntimeError('This transition cannot be executed on a subject in "{}" state, authorized source '
                               'states are {}.'.format(subject.state,
                                                       ', '.join(['"{}"'.format(state) for state in self.source]))
                               )
        try:
            retval = self.handler(self, subject, *args, **kwargs)
            subject.state = self.target
        except Exception as e:
            raise
        return retval

    @property
    def __name__(self):
        return self._name or self.handler.__name__

    def __repr__(self):
        return '<{}.{} object "{}" ({} to {}) at {}>'.format(
            type(self).__module__,
            type(self).__name__,
            self.__name__,
            '/'.join(self.source),
            self.target,
            hex(id(self)),
        )

    def handler(self, subject, *args, **kwargs):
        raise NotImplementedError('This is an abstract method that you should implement to have a working system.')


