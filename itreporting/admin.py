from django.contrib import admin
from .models import Issue
from .models import Course, Module, Registration

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Registration)
# Register your models here.
admin.site.register(Issue)

