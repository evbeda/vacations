from datetime import datetime

from django.test import TestCase, RequestFactory
from django.urls import reverse
from freezegun import freeze_time
from parameterized import parameterized

from vacations_app.models import (
    AssignedVacations,
    Employee,
    Vacation,
)


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


class AvailableVacationsTest(TestCase):

    @parameterized.expand([
        ('2019-12-01', '2019-07-01', 14, {2019: 14}),
        ('2020-05-01', '2019-07-01', 14, {2019: 14}),
        ('2019-12-01', '2019-07-01', 21, {2019: 21}),
        ('2020-05-01', '2019-07-01', 21, {2019: 21}),
        ('2019-12-01', '2019-08-05', 14, {2019: 5}),
        ('2019-12-31', '2019-12-30', 14, {}),
        ('2019-12-31', '2019-12-01', 14, {2019: 1}),
        ('2019-12-31', '2019-11-01', 14, {2019: 2}),
        ('2019-12-31', '2019-10-01', 14, {2019: 3}),
        ('2019-12-31', '2019-09-01', 14, {2019: 4}),
        ('2020-05-01', '2019-08-05', 14, {2019: 5}),
        ('2020-08-01', '2019-08-05', 14, {2019: 5, 2020: 14}),
        ('2021-08-01', '2019-08-05', 14, {2019: 5, 2020: 14, 2021: 14}),
        ('2020-08-01', '2019-07-01', 14, {2019: 14, 2020: 14}),
        ('2021-08-01', '2019-07-01', 14, {2019: 14, 2020: 14, 2021: 14}),
        ('2022-08-01', '2019-07-01', 14, {2019: 14, 2020: 14, 2021: 14, 2022: 14}),
        ('2023-08-01', '2019-07-01', 14, {2019: 14, 2020: 14, 2021: 14, 2022: 14, 2023: 14}),
        ('2024-08-01', '2019-07-01', 14, {2019: 14, 2020: 14, 2021: 14, 2022: 14, 2023: 14, 2024: 21}),
        ('2025-08-01', '2019-07-01', 14, {2019: 14, 2020: 14, 2021: 14, 2022: 14, 2023: 14, 2024: 21, 2025: 21}),
        ('2020-08-01', '2019-07-01', 21, {2019: 21, 2020: 21}),
        ('2021-08-01', '2019-07-01', 21, {2019: 21, 2020: 21, 2021: 21}),
        ('2022-08-01', '2019-07-01', 21, {2019: 21, 2020: 21, 2021: 21, 2022: 21}),
        ('2023-08-01', '2019-07-01', 21, {2019: 21, 2020: 21, 2021: 21, 2022: 21, 2023: 21}),
        ('2024-08-01', '2019-07-01', 21, {2019: 21, 2020: 21, 2021: 21, 2022: 21, 2023: 21, 2024: 28}),
        ('2025-08-01', '2019-07-01', 21, {2019: 21, 2020: 21, 2021: 21, 2022: 21, 2023: 21, 2024: 28, 2025: 28}),
        # Historic Employees dont have available vacations from 2018 by default
        ('2019-12-01', '2018-05-01', 14, {2019: 14}),
        ('2019-12-01', '2017-05-01', 14, {2019: 14}),
        ('2019-12-01', '2016-05-01', 14, {2019: 14}),
        ('2019-12-01', '2015-05-01', 14, {2019: 14}),
        ('2019-12-01', '2014-05-01', 14, {2019: 21}),
        ('2020-12-01', '2014-05-01', 14, {2019: 21, 2020: 21}),
        ('2021-12-01', '2014-05-01', 14, {2019: 21, 2020: 21, 2021: 21}),
        ('2022-12-01', '2014-05-01', 14, {2019: 21, 2020: 21, 2021: 21, 2022: 21}),
        ('2023-12-01', '2014-05-01', 14, {2019: 21, 2020: 21, 2021: 21, 2022: 21, 2023: 21}),
        ('2019-12-01', '2013-05-01', 14, {2019: 21}),
        ('2023-12-01', '2013-05-01', 14, {2019: 21, 2020: 21, 2021: 21, 2022: 21, 2023: 28}),
        ('2019-12-01', '2014-05-01', 21, {2019: 28}),
        ('2020-12-01', '2014-05-01', 21, {2019: 28, 2020: 28}),
        ('2021-12-01', '2014-05-01', 21, {2019: 28, 2020: 28, 2021: 28}),
        ('2022-12-01', '2014-05-01', 21, {2019: 28, 2020: 28, 2021: 28, 2022: 28}),
        ('2023-12-01', '2014-05-01', 21, {2019: 28, 2020: 28, 2021: 28, 2022: 28, 2023: 28}),
    ])
    def test_get_available_vacations(
        self,
        patch_now,
        job_start_date,
        initial_annual_vacations_days,
        available_vacations_expected,
    ):
        with freeze_time(patch_now):
            employee = Employee.objects.create(
                job_start_date=datetime.strptime(job_start_date, '%Y-%m-%d'),
                initial_annual_vacations_days=initial_annual_vacations_days,
            )
            available_vacations = employee.get_available_vacations()
        self.assertEqual(
            available_vacations,
            available_vacations_expected,
        )

    @parameterized.expand([
        # Historic Employees dont have available vacations from 2018 by default
        ('2019-12-01', '2018-05-01', 14, {2018: 7}, {2018: 7, 2019: 14}),
        ('2019-12-01', '2018-05-01', 14, {2017: 7, 2018: 14}, {2017: 7, 2018: 14, 2019: 14}),
        ('2023-12-01', '2014-05-01', 21, {2018: 14}, {2018: 14, 2019: 28, 2020: 28, 2021: 28, 2022: 28, 2023: 28}),
    ])
    def test_get_available_vacations_with_pending_vacations(
        self,
        patch_now,
        job_start_date,
        initial_annual_vacations_days,
        assigned_vacations,
        available_vacations_expected,
    ):
        with freeze_time(patch_now):
            employee = Employee.objects.create(
                job_start_date=datetime.strptime(job_start_date, '%Y-%m-%d'),
                initial_annual_vacations_days=initial_annual_vacations_days,
            )
            for assigned_vacation_year, assigned_vacation_days in assigned_vacations.items():
                AssignedVacations.objects.create(
                    worked_year=assigned_vacation_year,
                    total_days=assigned_vacation_days,
                    employee=employee,
                )
            available_vacations = employee.get_available_vacations()
        self.assertEqual(
            available_vacations,
            available_vacations_expected,
        )

    @parameterized.expand([
        ('2019-12-01', '2018-05-01', 14, {2018: 7}, {2018: 7, 2019: 7}, {2019: 7}),
        ('2023-12-01', '2014-05-01', 21, {2018: 14}, {2018: 14, 2019: 7}, {2019: 21, 2020: 28, 2021: 28, 2022: 28, 2023: 28}),
    ])
    def test_get_available_vacations_with_pending_vacations_with_vacations_requested(
        self,
        patch_now,
        job_start_date,
        initial_annual_vacations_days,
        assigned_vacations,
        vacations_requested,
        available_vacations_expected,
    ):
        with freeze_time(patch_now):
            employee = Employee.objects.create(
                job_start_date=datetime.strptime(job_start_date, '%Y-%m-%d'),
                initial_annual_vacations_days=initial_annual_vacations_days,
            )
            for vacation_year, vacation_days in vacations_requested.items():
                Vacation.objects.create(
                    from_date=datetime(vacation_year, 1, 1),
                    to_date=datetime(vacation_year, 1, 7),
                    days_quantity=vacation_days,
                    applicable_worked_year=vacation_year,
                    employee=employee,
                )
            for assigned_vacation_year, assigned_vacation_days in assigned_vacations.items():
                AssignedVacations.objects.create(
                    worked_year=assigned_vacation_year,
                    total_days=assigned_vacation_days,
                    employee=employee,
                )
            available_vacations = employee.get_available_vacations()
        self.assertEqual(
            available_vacations,
            available_vacations_expected,
        )
