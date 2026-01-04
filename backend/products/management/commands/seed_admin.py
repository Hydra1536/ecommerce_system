from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed default admin (superuser)"

    def handle(self, *args, **kwargs):
        email = "admin@example.com"
        password = "admin123"

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING("Admin user already exists.")
            )
            return

        # ERROR FIXED HERE: Removed first_name and last_name
        User.objects.create_superuser(
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS("Admin user created successfully.")
        )