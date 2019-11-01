# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory

# Create your tests here.
from django.urls import reverse
from social_core.tests.models import User

from vacations_app.models import Employee, Vacation


class HomeViewTest(TestCase):

    def SetUp(self):
        self.factory = RequestFactory()

        self.employee = Employee.objects.create(
            job_start_date = '2018-09-14',
            initial_annual_vacations_days = 14,
        )
        self.vacation = Vacation.objects.create(
            from_date = '2019-09-14',
            to_date = '2019-09-14',
            employee = self.employee,
        )
    def test_home_view(self):
        request = self.factory.get(reverse('home'))
        request.user = User.objects.create_user(
            username='test', email='test@test.com', password='secret')
        import ipdb;
        ipdb.set_trace()
