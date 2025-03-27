from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(post_save, sender=User)    
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('Created a new user profile')
    else:
        try:
            profile = instance.userprofile  # Directly use reverse relation
            profile.save()
            print('Updated user profile')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    print(f"About to save user: {instance.username}")
