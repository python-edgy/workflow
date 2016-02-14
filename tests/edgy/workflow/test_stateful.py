# -*- coding: utf-8 -*-

from unittest import TestCase

from .testutils.objects import StatefulSubject, InvalidStateful
from .testutils.factories import create_transition_to_duck, create_transition_to_pumpkin


class StatefulObjectsTest(TestCase):
    def test_stateful(self):
        obj = StatefulSubject(transitions=[
            create_transition_to_duck(),
            create_transition_to_pumpkin(),
        ])

        assert obj.state == 'human'

        obj.to_duck()

        assert obj.state == 'duck'

        with self.assertRaises(RuntimeError):
            obj.to_pumpkin()

        assert obj.state == 'duck'

    def test_invalid_stateful(self):
        with self.assertRaises(RuntimeError):
            InvalidStateful()

    def test_stateful_initial_state(self):
        obj = StatefulSubject(state='duck')
        assert obj.state == 'duck'

    def test_stateful_invalid_transition(self):
        obj = StatefulSubject()

        with self.assertRaises(AttributeError):
            obj.some_unknown_transition()

    def test_stateful_repr(self):
        obj = StatefulSubject(transitions=[
            create_transition_to_duck(),
            create_transition_to_pumpkin(),
        ])
        assert repr(obj).startswith('<{}.{} object with state "human" at '.format(
            StatefulSubject.__module__,
            StatefulSubject.__name__,
        ))

        obj.state = 'invalid'
        assert repr(obj).startswith('<{}.{} object with unknown state "invalid" at '.format(
            StatefulSubject.__module__,
            StatefulSubject.__name__,
        ))

