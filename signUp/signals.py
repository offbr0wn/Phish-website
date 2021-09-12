from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from django.contrib.auth.models import User


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#
#         Profile.objects.create(user=instance, name=instance.username, email=instance.email)
#         print("profile created")
#
#
# post_save.connect(create_profile, sender=User)


# def update_profile(sender, instance, created, **kwargs):
#     if created:
#         instance.profile.save()
#         print("profile updated")
#
#
# post_save.connect(update_profile, sender=User)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
