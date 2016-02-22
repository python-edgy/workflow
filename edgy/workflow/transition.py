# -*- coding: utf-8 -*-
"""
The smallest atom of ``edgy.workflow`` is a ``Transition``, which basically is a regular python
callable with additional metadata to make the system aware of when it can be applied.

"""

from edgy.workflow.constants import WILDCARD
from edgy.workflow.utils import issequence


class Transition(object):
    """
    Defines when and how to go from one state to another, eventually applying a user-defined
    side-effect while being applied.

    Example::

        >>> t = Transition(name='sleep', source='awake', target='asleep')

        >>> class Person(object):
        ...     state = 'awake'

        >>> me = Person()
        >>> t(me)
        >>> me.state
        'asleep'

    This class can also be used as a decorator::

        >>> @Transition(source='asleep', target='awake')

        >>> def wakeup(self, subject):
        ...     print('HEY!')

        >>> wakeup(me)
        >>> me.state
        'awake'

    A special wildcard source can make transitions work from any state. Just specify "*" as a
    transition source and you'll be able to transition from any state.

    """

    # Tracks each time a Transition instance is created. Used to retain order.
    creation_counter = 0

    # Transition handler. If absent, the transition is considered as "partial", and should be called with a handler
    # callable to be complete.
    handler = None

    def __init__(self, handler=None, name=None, source=None, target=None):
        self.source = tuple(source if issequence(source) else (source,))
        self.target = target
        self._name = name

        # Increase the creation counter, and save our local copy.
        self.creation_counter = Transition.creation_counter
        Transition.creation_counter += 1

        if handler:
            self.handler = handler or self.handler

    def __call__(self, *args, **kwargs):
        if self.handler:
            return self.__call_complete(*args, **kwargs)
        return self.__call_partial(*args, **kwargs)

    def __call_partial(self, handler):
        self.handler = handler
        return self

    def __call_complete(self, subject, *args, **kwargs):
        if not WILDCARD in self.source and not subject.state in self.source:
            raise RuntimeError(
                'This transition cannot be executed on a subject in "{}" state, authorized source '
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
        if self._name:
            return self._name
        if self.handler:
            return self.handler.__name__
        return 'partial'

    # Alias that can be used in django templates, for example.
    name = __name__

    def __repr__(self):
        return '<{}.{} object "{}" ({} to {}) at {}>'.format(
            type(self).__module__,
            type(self).__name__,
            self.__name__,
            '/'.join(self.source),
            self.target,
            hex(id(self)),
        )

