# -*- coding: utf-8 -*-

from django import forms

from edgy.workflow.ext.django_workflow.forms import TransitionForm
from example.workflow_app.models import Issue

class IssueForm(forms.models.ModelForm):

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
        ]
        widgets = {
            'title': forms.widgets.Input(attrs={'class': 'form-control'}),
            'description': forms.widgets.Textarea(attrs={'class': 'form-control'}),
        }

class IssueTransitionForm(TransitionForm):
    id = forms.fields.IntegerField(widget=forms.widgets.HiddenInput)

    class Meta:
        model = Issue
        fields = ['id', ]

