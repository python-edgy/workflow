# -*- coding: utf-8 -*-

from django.db import models

from edgy.workflow import StatefulObject


class StatefulModel(StatefulObject, models.Model):
    pass
