# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from edgy.workflow import Workflow, Transition, StatefulObject

workflow = Workflow()

@Transition(source='new', target='accepted')
def accept(self, subject):
    print('accepting {} using {}...'.format(subject, self))

@Transition(source='new', target='refused')
def refuse(self, subject):
    print('refusing {} using {}...'.format(subject, self))

workflow.add_transition(accept)
workflow.add_transition(refuse)

class Issue(StatefulObject):
    initial_state = 'new'
    workflow = workflow

iss42 = Issue()
print(iss42)

iss42.accept()
print(iss42)

iss43 = Issue()
print(iss43)

iss43.refuse()
print(iss43)

iss44 = Issue(state='invalid')
print(iss44)


