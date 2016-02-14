# -*- coding: utf-8 -*-

from unittest import TestCase

from edgy.workflow import Workflow
from .testutils.factories import create_transition_to_duck, create_transition_to_pumpkin, create_subject


class BasicTest(TestCase):
    def test_workflow(self):
        # create a workflow
        workflow = Workflow()
        assert len(workflow._transitions) == 0

        # add an invalid transition
        with self.assertRaises(AttributeError):
            workflow.add_transition(object())
        assert len(workflow._transitions) == 0

        # add our "to_duck" transition to our workflow
        to_duck = create_transition_to_duck()
        workflow.add_transition(to_duck)

        # create a stateful subject
        subject = create_subject()

        # check we can see our transition as available
        available_transitions = workflow.get_available_transitions_for(subject)
        assert available_transitions['to_duck'] == to_duck
        assert len(available_transitions) == 1

        # execute transition and check our subject is now a duck
        to_duck(subject)
        assert subject.is_duck
        assert subject.state == 'duck'

    def test_transition(self):
        to_duck = create_transition_to_duck()
        to_pumpkin = create_transition_to_pumpkin()

        subject = create_subject()

        to_pumpkin(subject)
        assert subject.is_pumpkin

        # this transition only works on humans.
        with self.assertRaises(RuntimeError):
            to_pumpkin(subject)

        to_duck(subject)
        assert not subject.is_pumpkin
        assert subject.is_duck

        # this transition only works on humans.
        with self.assertRaises(RuntimeError):
            to_pumpkin(subject)
