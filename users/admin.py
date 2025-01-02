from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Profile
from .forms import ProfileAdminForm

#class ProfileAdminForm(ModelForm):
 #   class Meta:
  #      model = Profile

   # def clean_user(self):
    #    user = self.cleaned_data['user']
     #   if user.groups.count() > 1:
      #      raise ValidationError("A user cannot belong to more than one group.")
       # return user

#class ProfileAdmin(admin.ModelAdmin):
 #   list_display = ['user', 'date_of_birth', 'address', 'city', 'country', 'image']
  #  search_fields = ['user__username', 'user__first_name', 'user__last_name']
   # list_filter = ['country']
    #readonly_fields = ['user']  # Make 'user' read-only if necessary
    #form = ProfileAdminForm 

#class ProfileAdmin(admin.ModelAdmin):
 #   form = ProfileAdminForm
 
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm

    def save_model(self, request, obj, form, change):
        # Ensure the user is assigned to only one group
        if obj.user.groups.count() > 1:
            raise ValidationError("A user can only be assigned to one group.")
        super().save_model(request, obj, form, change)

admin.site.register(Profile, ProfileAdmin)