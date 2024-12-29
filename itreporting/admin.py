from django.contrib import admin
from .models import Issue
from .models import Course, Module, Registration

# Register your models here.
admin.site.register(Issue)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'date_registered')
    search_fields = ('student__username', 'module__name')
    list_filter = ('date_registered',)

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Registration, RegistrationAdmin)