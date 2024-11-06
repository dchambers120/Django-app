from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'itreporting/home.html', {'title': 'Welcome to our Home Page'})
def about(request):
    return render(request, 'itreporting/about.html', {'title': 'Welcome to the About Page'})
def contact(request):
    return render(request, 'itreporting/contact.html', {'title': 'Welcome to the Contact Page'})
# Create your views here.
