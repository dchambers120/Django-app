from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Issue
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
import requests
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from .models import Module, Course, Registration
from django.contrib import messages

def home(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK'), ('Melaka', 'Malaysia'), ('Bandung', 'Indonesia')]
    weather_data = []
    api_key = '997409d38e16ba2ba15339c311fbf62a'

    for city in cities:
        # Request the API data and convert the JSON to Python data types
        
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json()

        print(city_weather)
        weather = {
            'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description']
        }
        weather_data.append(weather)  # Add the data for the current city into our list
        
    courses = Course.objects.all()
    
    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data, 'courses': courses,})

def about(request):
    return render(request, 'itreporting/about.html', {'title': 'Welcome to the About Page'})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            
            html = render_to_string('itreporting/emails/contactform.html', {
                'name': name,
                'email': email,
                'content': content
            })
            
            send_mail('The contact form subject', 'This is the message', 'declan@gmail.com', ['declanchambers83@gmail.com'], html_message=html)
            
            return redirect('contact')
 
    else:
        form = ContactForm
        
    return render(request, 'itreporting/contact.html',{'form': form })

def report(request):
    daily_report = {'issues': Issue.objects.all(), 'title': 'Issues Reported'}
    return render(request, 'itreporting/report.html', daily_report)

@login_required
def module_list(request):
    # Fetch all modules and the modules that the student is already registered for
    modules = Module.objects.all()
    registered_modules = Registration.objects.filter(student=request.user).values_list('module', flat=True)

    return render(request, 'itreporting/module_list.html', {
        'modules': modules,
        'registered_modules': registered_modules,  # Registered modules for the current student
    })

@login_required
def register_module(request, module_id):
    if not request.user.is_authenticated:
        return redirect('login')

    module = get_object_or_404(Module, id=module_id)

    # Check if the student is already registered for this module
    if Registration.objects.filter(student=request.user, module=module).exists():
        messages.error(request, f"You are already registered for the module: {module.name}.")
        return redirect('itreporting:module_list')  # Adjust as per the page where this is displayed

    # Create a new registration
    Registration.objects.create(student=request.user, module=module)
    messages.success(request, f"You have successfully registered for the module: {module.name}.")
    return redirect('itreporting:module_list')
    
@login_required
def unregister_module(request, module_id):
    if not request.user.is_authenticated:
        return redirect('login')

    module = get_object_or_404(Module, id=module_id)

    # Check if the student is registered for this module
    registration = Registration.objects.filter(student=request.user, module=module).first()
    if registration:
        registration.delete()
        messages.success(request, f"You have successfully unregistered from the module: {module.name}.")
    else:
        messages.error(request, f"You are not registered for the module: {module.name}.")

    return redirect('itreporting:module_list')

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'itreporting/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.module_set.all()  # Retrieve all modules related to this course
    return render(request, 'itreporting/course_detail.html', {'course': course, 'modules': modules})

@login_required
def my_registrations(request):
    # Get modules registered by the logged-in user
    registered_modules = Registration.objects.filter(student=request.user)

    return render(request, 'itreporting/my_registrations.html', {
        'registered_modules': registered_modules,
    })

class PostListView(ListView):
    model = Issue
    ordering = ['-date_submitted']
    template_name = 'itreporting/report.html'
    context_object_name = 'issues'
    paginate_by = 5 # Optional 
    
class UserPostListView(ListView): 

    model = Issue
    template_name = 'itreporting/user_issues.html' 
    context_object_name = 'issues'
    paginate_by = 5


    def get_queryset(self):

        user=get_object_or_404(User, username=self.kwargs.get('username'))

        return Issue.objects.filter(author=user).order_by('-date_submitted')

    
class PostDetailView(DetailView):
    model = Issue
    template_name = 'itreporting/issue_detail.html'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Issue   
    fields = ['type', 'room', 'urgent', 'details']
    
    def form_valid(self, form):
    
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Issue
    fields = ['type', 'room', 'details']
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Issue
    success_url = '/report'
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.author
    
    

