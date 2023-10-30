from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver, Signal
from .models import User, Profile


@receiver(post_save, sender=User)
def create_profile_with_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, first_name=instance.username)

