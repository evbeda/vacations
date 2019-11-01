# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Employee(User):
    job_start_date = models.DateField()
    initial_annual_vacations_days = models.IntegerField(default=14)


class Vacation(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    employee = models.ForeignKey('Employee')
