# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .models import Vacation

# Create your views here.
class HomeView(TemplateView):
    template_name= 'vacations_app/index.html'


# Create your views here.
class VacationPrintView(DetailView):
    template_name= 'vacations_app/vacation_print_form.html'
    model = Vacation