from django.contrib import admin
from .models import Issue
from .models import Course, Module, Registration
from django.core.exceptions import ValidationError

# Register your models here.
admin.site.register(Issue)

class RegistrationAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Ensure the student is not already registered for the module
        if Registration.objects.filter(student=obj.student, module=obj.module).exists():
            raise ValidationError("A student can only register for one module.")

        super().save_model(request, obj, form, change)

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Registration, RegistrationAdmin)