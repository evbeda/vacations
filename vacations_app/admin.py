# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    AssignedVacations,
    Employee,
    Holiday,
    Team,
    Vacation,
)

admin.site.register(Employee)
admin.site.register(Vacation)
admin.site.register(Holiday)
admin.site.register(Team)
admin.site.register(AssignedVacations)
