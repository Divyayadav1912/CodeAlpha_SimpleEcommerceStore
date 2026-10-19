
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create an admin user using environment variables"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL", "")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not password:
            self.stderr.write(
                "Set ADMIN_USERNAME and ADMIN_PASSWORD first."
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write("This admin username already exists.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(
            self.style.SUCCESS("Admin user created successfully.")
        )
