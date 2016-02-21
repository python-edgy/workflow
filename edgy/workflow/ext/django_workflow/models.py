# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from django.db import models

from edgy.workflow import StatefulObject


class StatefulModel(StatefulObject, models.Model):
    pass
