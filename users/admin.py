from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'address', 'city', 'country', 'image']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['country']
    readonly_fields = ['user']  # Make 'user' read-only if necessary

admin.site.register(Profile, ProfileAdmin)