from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        if os.getenv("RENDER") != "True":
            return

        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")

        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
