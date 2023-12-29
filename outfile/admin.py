from django.contrib import admin

# Register your models here.

from .models import Problem, InputOutput
admin.site.register(Problem)
admin.site.register(InputOutput)
