# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView
from vacations_app.models import Employee


# Create your views here.


class HomeView(ListView):
    template_name= 'vacations_app/index.html'
    model = Employee