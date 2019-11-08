from django.test import TestCase, RequestFactory
from django.urls import reverse

from vacations_app.models import Employee, Vacation


class HomeViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.employee = Employee.objects.create(
            job_start_date = '2018-09-14',
            initial_annual_vacations_days = 14,
        )
        self.vacation = Vacation.objects.create(
            from_date = '2019-09-14',
            to_date = '2019-09-15',
            days_quantity = 2,
            applicable_worked_year = 2018,
            employee = self.employee,
        )
    def test_home_view(self):
        request = self.factory.get(reverse('home'))
        request.user = Employee.objects.create_user(
            email='test@test.com',
            password='secret',
        )
