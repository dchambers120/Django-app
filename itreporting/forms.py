from django import forms 
from .models import Registration
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['student', 'module']

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get("student")
        
        if student and Registration.objects.filter(student=student).exists():
            raise ValidationError("A student can only register for one module.")
        
        return cleaned_data   