from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView

from edgy.workflow.ext.django_workflow.views import TransitionView
from example.workflow_app.forms import IssueTransitionForm, IssueForm
from example.workflow_app.models import  Issue


class IssueMixin(object):
    model = Issue


class IssueListView(IssueMixin, ListView):
    pass


class IssueCreateView(IssueMixin, CreateView):
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue-list')


class IssueDetailView(IssueMixin, DetailView):
    pass


class IssueTransitionView(IssueMixin, TransitionView):
    form_class = IssueTransitionForm
    template_name = 'workflow_app/issue_transition.html'
