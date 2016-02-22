from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from edgy.workflow import StatefulObject, Workflow, Transition


class IssueWorkflow(Workflow):
    @Transition(source='new', target='ready')
    def accept(self, subject):
        pass

    @Transition(source='new', target='refused')
    def refuse(self, subject):
        pass

    @Transition(source='ready', target='in_progress')
    def start(self, subject):
        pass

    @Transition(source='in_progress', target='done')
    def complete(self, subject):
        pass

    @Transition(source='done', target='closed')
    def close(self, subject):
        pass

    @Transition(source='*', target='invalid')
    def invalidate(self, subject):
        pass

    @Transition(source='*', target='new')
    def reset(self, subject):
        pass


class Issue(StatefulObject, models.Model):
    default_state = 'new'
    workflow = IssueWorkflow()

    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='authored_issues',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_issues',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    state = models.CharField(max_length=255, default='new')

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={
            'pk': self.pk
        })

