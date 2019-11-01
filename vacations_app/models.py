# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.db.models.aggregates import Sum
from django.contrib.auth.models import User, UserManager


class Employee(User):
    job_start_date = models.DateField()
    initial_annual_vacations_days = models.IntegerField(default=14)


class Vacation(models.Model):
    pepe = UserManager()
    from_date = models.DateField()
    to_date = models.DateField()
    employee = models.ForeignKey('Employee')
    applicable_worked_year = models.IntegerField()

    @property
    def to_date_next_day(self):
        return self.to_date + timedelta(days=1)

    @property
    def year_vacation_left(self):
        vacations = Vacation.objects.filter(
            employee=self.employee,
            applicable_worked_year=self.applicable_worked_year,
        )
        total = 0
        for vacation in vacations:
            vacation_diff = vacation.to_date - vacation.from_date
            total += vacation_diff.days
        return self.employee.initial_annual_vacations_days - total

