from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Profile

# Signal to create a profile when a new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile only once when the user is created
        Profile.objects.create(user=instance)
        
# Signal to save the profile when the user is saved (if needed)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Only save the profile if it exists (no duplicate creation)
    if hasattr(instance, 'profile'):
        instance.profile.save()

# Signal to manage user groups
@receiver(post_save, sender=User)
def manage_user_group(sender, instance, created, **kwargs):
    if created:
        # Assign the user to a default group if they're newly created
        group_name = 'default_group'
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.clear()  # Remove any existing groups
        instance.groups.add(group)  # Add the user to the selected group
    else:
        # Ensure the user belongs to only one group
        if instance.groups.count() > 1:
            # Remove the user from all groups except the first one
            instance.groups.all()[1:].delete()

            
