# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from edgy.workflow import Workflow, Transition, StatefulObject


class MyWorkflow(Workflow):
    @Transition(source='new', target='accepted')
    def accept(self, subject):
        print('accepting {} using {}...'.format(subject, self))

    @Transition(source='new', target='refused')
    def refuse(self, subject):
        print('refusing {} using {}...'.format(subject, self))


class Issue(StatefulObject):
    initial_state = 'new'
    workflow = MyWorkflow()


print('>>> iss42 = Issue()')
iss42 = Issue()
print('iss42 =', iss42)

iss42.accept()
print('iss42 =', iss42)

print('>>> iss43 = Issue()')
iss43 = Issue()
print('iss43 =', iss43)

iss43.refuse()
print('iss43 =', iss43)

print('>>> iss44 = Issue(state="invalid")')
iss44 = Issue(state='invalid')
print('iss44 =', iss44)
