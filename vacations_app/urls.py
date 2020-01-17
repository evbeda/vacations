"""vacations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import (
    AssignedVacationCreateView,
    AssignedVacationDeleteView,
    AssignedVacationsListView,
    AssignedVacationUpdateView,
    EmployeeCreateView,
    EmployeeListView,
    EmployeeUpdateView,
    AutoHolidayView,
    HolidayCreateView,
    HolidayUpdateView,
    HolidayDeleteView,
    HolidayListView,
    HomeView,
    TeamCreateView,
    TeamDeleteView,
    TeamListView,
    TeamVacationsListView,
    TeamUpdateView,
    AdminVacationRequest,
    AdminVacationRequestDeleteView,
    VacationDownloadListView,
    VacationListView,
    VacationPrintView,
    VacationRequest,
)


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^teams$', TeamListView.as_view(), name='team-list'),
    url(r'^teams/create$', TeamCreateView.as_view(), name='team-create'),
    url(r'^teams/update/(?P<pk>[0-9]+)/$', TeamUpdateView.as_view(), name='team-update'),
    url(r'^teams/delete/(?P<pk>[0-9]+)/$', TeamDeleteView.as_view(), name='team-delete'),
    url(r'^employees$', EmployeeListView.as_view(), name='employees-list'),
    url(r'^employees/create$', EmployeeCreateView.as_view(), name='employee-create'),
    url(r'^employees/update/(?P<pk>[0-9]+)/$', EmployeeUpdateView.as_view(), name='employee-update'),
    url(r'^vacation/request$', VacationRequest.as_view(), name='vacation-request'),
    url(r'^vacation/admin-request$', AdminVacationRequest.as_view(), name='vacation-admin-request'),
    url(r'^vacation/admin-request/delete/(?P<pk>[0-9]+)/$', AdminVacationRequestDeleteView.as_view(), name='vacation-admin-delete'),
    url(r'^vacations$', VacationListView.as_view(), name='vacations-list'),
    url(r'^vacations/download$', VacationDownloadListView.as_view(), name='vacations-download'),
    url(r'^vacations/team$', TeamVacationsListView.as_view(), name='vacations-team'),
    url(r'^assigned_vacations$', AssignedVacationsListView.as_view(), name='assigned-vacations-list'),
    url(r'^assigned_vacations/create$', AssignedVacationCreateView.as_view(), name='assigned-vacations-create'),
    url(r'^assigned_vacations/update/(?P<pk>[0-9]+)/$', AssignedVacationUpdateView.as_view(), name='assigned-vacations-update'),
    url(r'^assigned_vacations/delete/(?P<pk>[0-9]+)/$', AssignedVacationDeleteView.as_view(), name='assigned-vacations-delete'),
    url(r'^holidays$', HolidayListView.as_view(), name='holidays-list'),
    url(r'^holidays/auto_create$', AutoHolidayView.as_view(), name='holidays-auto-create'),
    url(r'^holidays/create$', HolidayCreateView.as_view(), name='holidays-create'),
    url(r'^holidays/update/(?P<pk>[0-9]+)/$', HolidayUpdateView.as_view(), name='holidays-update'),
    url(r'^holidays/delete/(?P<pk>[0-9]+)/$', HolidayDeleteView.as_view(), name='holidays-delete'),
    url(r'^print/(?P<pk>[0-9]+)/$', VacationPrintView.as_view(), name='print'),
]
