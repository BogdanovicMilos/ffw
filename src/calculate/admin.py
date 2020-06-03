from django.contrib import admin
from calculate.models import Calculate


class CalculateAdmin(admin.ModelAdmin):
    list_display = ['array', 'calculations']


admin.site.register(Calculate, CalculateAdmin)
