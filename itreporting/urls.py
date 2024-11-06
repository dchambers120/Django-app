from django.urls import path
from . import views

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('', views.about, name = 'about'),
    path('', views.contact, name = 'contact')
    ]


