from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm
from .models import Profile
import requests

# Create your views here.
#def register(request):
 #   if request.method == 'POST':
  #      form = UserRegisterForm(request.POST)
   #     if form.is_valid():
    #        form.save()
     #       username = form.cleaned_data.get('username')
      #      messages.success(request, f'Your account has been created! Now you can login!')
       #     return redirect('login')
        #else:
         #   messages.warning(request, 'Unable to create account.')
    #else:
     #   form = UserRegisterForm()
    #return render(request, 'users/register.html', {'form': form, 'title': 'Student Registration'})
#@login_required

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save user form
            user = user_form.save()
            
            # Check if the profile already exists for this user
            profile, created = Profile.objects.get_or_create(user=user)

            # Save profile form
            if created:
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! Now you can login!')
            return redirect('login')
        else:
            messages.warning(request, 'Unable to create account. Please check the form fields.')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Student Registration'
    })

#def profile(request):
 #   if request.method == 'POST':
  #      u_form = UserUpdateForm(request.POST, instance=request.user)
   #     p_form= ProfileUpdateForm(request.POST, request.FILES,
    #instance=request.user.profile)
            
     #   if u_form.is_valid() and p_form.is_valid():
      #      u_form.save()
       #     p_form.save()
        #    messages.success(request, 'Your account has been successfully updated!')
        #return redirect('profile')
    #else:
     #   u_form = UserUpdateForm(instance = request.user)
      #  p_form = ProfileUpdateForm(instance = request.user.profile)
       # context = {'u_form': u_form, 'p_form': p_form, 'title': 'Student Profile'}
        #return render(request, 'users/profile.html', context)
       
       
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Replace 'profile' with your profile page URL name.
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)


def home(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid={}'
    cities = [('Sheffield', 'UK')]
    weather_data = []
    api_key = '<997409d38e16ba2ba15339c311fbf62a>'

    for city in cities:
        city_weather = requests.get(url.format(city[0], city[1], api_key)).json() # Request the API data and convert the JSON to Python data types

    weather = {
        'city': city_weather['name'] + ', ' + city_weather['sys']['country'],
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description']
    }   
    weather_data.append(weather) # Add the data for the current city into our list
    return render(request, 'itreporting/home.html', {'title': 'Homepage', 'weather_data': weather_data})

