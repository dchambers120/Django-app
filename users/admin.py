from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Profile
from .forms import ProfileAdminForm
 
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm

    def save_model(self, request, obj, form, change):
        # Ensure the user is assigned to only one group
        if obj.user.groups.count() > 1:
            raise ValidationError("A user can only be assigned to one group.")
        super().save_model(request, obj, form, change)

admin.site.register(Profile, ProfileAdmin)