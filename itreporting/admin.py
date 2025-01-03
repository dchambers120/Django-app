from django.contrib import admin
from .models import Issue
from .models import Course, Module, Registration
from django.core.exceptions import ValidationError

# Register your models here.
admin.site.register(Issue)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'date_registered')
    search_fields = ('student__username', 'module__name')
    list_filter = ('date_registered',)
    
    def save_model(self, request, obj, form, change):
        # Ensure the student is not already registered for another module
        if Registration.objects.filter(student=obj.student).exists():
            raise ValidationError("A student can only register for one module.")
        
        # Proceed to save the registration
        super().save_model(request, obj, form, change)

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Registration, RegistrationAdmin)