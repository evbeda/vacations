# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


def is_holiday(day):
    return bool(Holiday.objects.filter(date=day))


def validate_from_date(value):
    if is_holiday(value):
        raise ValidationError("You can't choose a holiday.")
    if value.weekday() == 0:
        return value
    previous_monday = value - timedelta(value.weekday())
    for i in range((value - previous_monday).days):
        if not is_holiday(previous_monday):
            raise ValidationError('You must choose the first working day of the week.')
        previous_monday += timedelta(days=1)
    return value


def validate_year(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(f'The applicable worked year can not be greater than {current_year}')
    else:
        return value


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    job_start_date = models.DateField(null=True)
    initial_annual_vacations_days = models.IntegerField(default=14)
    team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL,
        related_name='members',
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Vacation(models.Model):

    from_date = models.DateField()
    days_quantity = models.IntegerField()
    to_date = models.DateField()
    employee = models.ForeignKey('Employee')
    applicable_worked_year = models.IntegerField(validators=[validate_year])

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


class Holiday(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(unique=True)

    def __str__(self):
        return f'{self.date.year} - {self.name}'


class Team(models.Model):
    name = models.CharField(max_length=30)
    engineer_manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_teams',
    )

    def __str__(self):
        return self.name


class AssignedVacations(models.Model):
    worked_year = models.IntegerField()
    total_days = models.IntegerField()
    employee = models.ForeignKey('Employee')

    def __str__(self):
        return f'{self.worked_year} - {self.total_days} days'
