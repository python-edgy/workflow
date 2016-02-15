# -*- coding: utf-8 -*-

from edgy.workflow import Transition

from .objects import Subject


def create_transition_to_pumpkin():
    @Transition(source='human', target='pumpkin')
    def to_pumpkin(self, subject):
        subject.is_duck, subject.is_pumpkin = False, True
    assert to_pumpkin.__name__ == 'to_pumpkin'
    assert to_pumpkin.target == 'pumpkin'
    assert to_pumpkin.source == ('human', )
    return to_pumpkin


def create_transition_to_duck():
    @Transition(source='*', target='duck')
    def to_duck(self, subject):
        subject.is_duck, subject.is_pumpkin = True, False
    assert to_duck.__name__ == 'to_duck'
    assert to_duck.target == 'duck'
    assert to_duck.source == ('*', )
    return to_duck


def create_subject(**kwargs):
    subject = Subject(**kwargs)
    assert subject.state == 'human'
    return subject
