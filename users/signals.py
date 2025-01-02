from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   instance.profile.save()

@receiver(post_save, sender=User)
def manage_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
        
@receiver(post_save, sender=User)
def manage_user_group(sender, instance, created, **kwargs):
    if created:
        # If the user is newly created, we add them to a default group (e.g., 'default_group')
        group_name = 'default_group'
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.clear()  # Remove any existing groups
        instance.groups.add(group)  # Add the user to the selected group
    else:
        # If user is updated, ensure only one group is assigned
        if instance.groups.count() > 1:
            # Remove the user from all groups except the first one
            instance.groups.all()[1:].delete()