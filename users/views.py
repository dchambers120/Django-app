from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm
from django.db import transaction
from .models import Profile
import requests

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    # Save the user
                    user = user_form.save()

                    # Safeguard against duplicates by using update_or_create
                    profile, created = Profile.objects.update_or_create(
                        user=user,
                        defaults={
                            'bio': profile_form.cleaned_data.get('bio', ''),
                            # Add other fields as necessary
                        }
                    )

                messages.success(request, 'Your account has been created! You can now log in.')
                return redirect('login')
            except Exception as e:
                print(f"Error occurred: {e}")
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Student Registration',
    })
    
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the user info
            profile_form.save()  # Save the profile updates
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile page after successful update
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

