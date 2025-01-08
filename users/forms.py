from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'date_of_birth', 'address', 'city', 'country', 'photo']
        
class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'address', 'city', 'country', 'photo']
        
class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        
    def clean_user(self):
        user = self.cleaned_data.get('user')

        # Ensure the user is assigned to only one group
        if user.groups.count() > 1:
            raise ValidationError("A user can only be assigned to one group.")
        return user
    