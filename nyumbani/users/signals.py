import firebase_admin

from django.dispatch import receiver
from django.db.models.signals import post_save

from djoser.signals import user_registered

from firebase_admin import credentials
from firebase_admin import auth
from django.contrib.auth import get_user_model
from users.models import UserProfile, User

from django.conf import settings

User = get_user_model()

FIREBASE_USERS_URL = f"{settings.SUPABASE_BASE_URL}/firebase_users"


@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, *args, **kwargs):
    user = instance
    if not created:
        return
