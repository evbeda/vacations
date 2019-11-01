# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView
from vacations_app.models import Employee
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import Vacation

# Create your views here.


class HomeView(ListView):
    template_name= 'vacations_app/index.html'
    # model = Vacation

    def get_queryset(self):
        queryset = Vacation.objects.filter(employee_id=1)
        return queryset.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context





# Create your views here.
class VacationPrintView(DetailView):
    template_name= 'vacations_app/vacation_print_form.html'
    model = Vacation
