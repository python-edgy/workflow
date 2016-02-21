# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView


class TransitionView(SingleObjectTemplateResponseMixin, BaseUpdateView):
    def get_form_kwargs(self):
        form_kwargs = super(TransitionView, self).get_form_kwargs()
        form_kwargs['transition'] = self.transition
        return form_kwargs

    def dispatch(self, request, *args, **kwargs):
        self.transition = kwargs.pop('transition')
        return super(TransitionView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(TransitionView, self).get_context_data(**kwargs)
        context_data['transition'] = self.transition
        return context_data

