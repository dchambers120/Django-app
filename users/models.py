from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')
    
    def __str__(self):
        return f'{self.user.username}'
