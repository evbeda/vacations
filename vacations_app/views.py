# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import BytesIO
from datetime import timedelta

from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
    UpdateView,
)
from xhtml2pdf import pisa

from vacations_app import (
    CAN_VIEW_OTHER_VACATIONS,
    CAN_VIEW_TEAM_MEMBERS_VACATIONS,
)
from vacations_app.models import (
    AssignedVacations,
    Holiday,
    Vacation,
    validate_from_date,
)


class HomeView(ListView):
    template_name = 'vacations_app/index.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Vacation.objects.filter(employee=self.request.user)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff_user'] = self.request.user.has_perm('vacations_app.can_view_other_vacations')
        context['manager_user'] = self.request.user.has_perm('vacations_app.can_view_team_members_vacations')
        return context


class BaseVacationRequest(CreateView):
    model = Vacation
    success_url = reverse_lazy('home')

    def get_form(self):
        form = super().get_form()
        form.fields['applicable_worked_year'] = forms.ChoiceField(
            choices=(
                (2016, 2016, ),
                (2017, 2017, ),
                (2018, 2018, ),
                (2019, 2019, ),
            )
        )
        return form

    def form_valid(self, form):
        days = form.instance.days_quantity
        form.instance.to_date = form.instance.from_date + timedelta(days=days)
        return super().form_valid(form)


class VacationRequest(BaseVacationRequest):
    template_name = 'vacations_app/vacation_request.html'
    fields = ['from_date', 'days_quantity', 'applicable_worked_year']

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'] = forms.DateField(
            widget=DatePickerInput(),
            validators=[validate_from_date],
        )
        form.fields['days_quantity'] = forms.ChoiceField(
            choices=(
                (7, 7),
                (14, 14),
                (21, 21),
                (28, 28),
            )
        )
        return form

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class AdminVacationRequest(BaseVacationRequest):
    template_name = 'vacations_app/admin_vacation_request.html'
    fields = ['employee', 'from_date', 'days_quantity', 'applicable_worked_year']

    def get_form(self):
        form = super().get_form()
        form.fields['from_date'] = forms.DateField(
            widget=DatePickerInput(),
        )
        return form


class VacationList(PermissionRequiredMixin, ListView):
    template_name = 'vacations_app/vacation-list.html'
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = Vacation


class TeamVacationsList(PermissionRequiredMixin, ListView):
    template_name = 'vacations_app/team-vacations-list.html'
    permission_required = CAN_VIEW_TEAM_MEMBERS_VACATIONS

    def get_queryset(self):
        managed_teams = self.request.user.managed_teams.all()
        all_vacations = Vacation.objects.filter(employee__team__in=managed_teams)
        vacations_by_team = {
            team.name: all_vacations.filter(employee__team=team)
            for team in managed_teams
        }
        return vacations_by_team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = [team.name for team in self.request.user.managed_teams.all()]
        return context


class VacationPrintView(DetailView):
    template_name = 'vacations_app/vacation_print_form.html'
    model = Vacation

    def render_to_response(self, context, **response_kwargs):
        pdf = render_to_pdf(self.template_name, context)
        return HttpResponse(pdf, content_type='application/pdf')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    return HttpResponse(result.getvalue(), content_type='application/pdf') if not pdf.err else None


class HolidayList(PermissionRequiredMixin, ListView):
    template_name = 'vacations_app/holiday-list.html'
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = Holiday


class HolidayCreateView(PermissionRequiredMixin, CreateView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = Holiday
    fields = '__all__'
    success_url = reverse_lazy('holidays-list')

    def get_form(self):
        form = super().get_form()
        form.fields['date'] = forms.DateField(
            widget=DatePickerInput(),
        )
        return form


class HolidayDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = Holiday
    success_url = reverse_lazy('holidays-list')


class HolidayUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = Holiday
    fields = '__all__'
    success_url = reverse_lazy('holidays-list')

    def get_form(self):
        form = super().get_form()
        form.fields['date'] = forms.DateField(
            widget=DatePickerInput(),
        )
        return form


class AssignedVacationsList(PermissionRequiredMixin, ListView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = AssignedVacations


class AssignedVacationCreateView(PermissionRequiredMixin, CreateView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = AssignedVacations
    fields = '__all__'
    success_url = reverse_lazy('assigned-vacations-list')


class AssignedVacationUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = AssignedVacations
    fields = '__all__'
    success_url = reverse_lazy('assigned-vacations-list')


class AssignedVacationDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = CAN_VIEW_OTHER_VACATIONS
    model = AssignedVacations
    success_url = reverse_lazy('assigned-vacations-list')
