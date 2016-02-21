# -*- coding: utf-8 -*-

from django import forms

class TransitionForm(forms.models.ModelForm):
    def __init__(self, *args, **kwargs):
        self.transition = kwargs.pop('transition')
        super(TransitionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        transition_handler = getattr(self.instance, self.transition)
        try:
            transition_handler()
            return super(TransitionForm, self).save(commit=commit)
        except Exception as e:
            # TODO rollback
            raise

