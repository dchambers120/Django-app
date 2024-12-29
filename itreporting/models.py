from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Issue(models.Model):
    type = models.CharField(max_length=100, choices = [('Hardware', 'Hardware'), ('Software', 'Software')])
    room = models.CharField(max_length=100)
    urgent = models.BooleanField(default = False)
    details = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    author = models.ForeignKey(User, related_name = 'issues',
    on_delete=models.CASCADE)
    def __str__(self):

        return f'{self.type} Issue in {self.room}'

def get_absolute_url(self):
  
    return reverse('itreporting:issue-detail', kwargs =
{'pk': self.pk})
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credit = models.IntegerField()
    category = models.CharField(max_length=50)
    description = models.TextField()
    availability = models.BooleanField(default=True)  
    courses_allowed = models.ManyToManyField(Course)  

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'module'], name='unique_registration')
        ]

    def __str__(self):
        return f"{self.student.username} registered for {self.module.name}"
    
