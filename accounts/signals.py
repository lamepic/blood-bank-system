from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import UserProfile, StaffProfile

User = get_user_model()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_normalUser:
            UserProfile.objects.create(
                user=instance,
            )

post_save.connect(create_user_profile, sender=User)


def create_staff_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staffUser:
            StaffProfile.objects.create(
                user=instance
            )
post_save.connect(create_staff_profile, sender=User)
