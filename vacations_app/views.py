# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from vacations_app.models import Vacation
from xhtml2pdf import pisa

from .models import Vacation


class HomeView(ListView):
    template_name= 'vacations_app/index.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Vacation.objects.filter(employee=self.request.user)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class VacationRequest(CreateView):
    template_name='vacations_app/vacation_request.html'
    model = Vacation
    fields = ['from_date', 'to_date', 'applicable_worked_year']

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        form.instance.employee = self.request.user
        return super().form_valid(form)


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
