from psycopg import OperationalError as PsycopgOperationalError

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError as DjangoOperationalError
from django.db import transaction

from core.settings import env

User = get_user_model()


class Command(BaseCommand):
    help = "Create the first staff superuser from environment variables."

    def handle(self, *args, **options):
        username = env("ADMIN_USERNAME", default="").strip()
        email = env("ADMIN_EMAIL", default="").strip()
        password = env("ADMIN_PASSWORD", default="").strip()
        database_url = env("DATABASE_URL", default="").strip()

        if not username or not email or not password:
            raise CommandError(
                "Missing admin seed variables. Set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD in .env."
            )

        try:
            existing_user = (
                User.objects.filter(username=username).first()
                or User.objects.filter(email__iexact=email).first()
            )
        except (DjangoOperationalError, PsycopgOperationalError) as exc:
            raise CommandError(self._build_database_error_message(database_url, exc)) from exc

        if existing_user:
            self.stdout.write(
                self.style.WARNING(
                    f"Admin already exists for username '{existing_user.username}'. Skipping seed."
                )
            )
            return

        try:
            with transaction.atomic():
                admin_user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_active=True,
                )
        except (DjangoOperationalError, PsycopgOperationalError) as exc:
            raise CommandError(self._build_database_error_message(database_url, exc)) from exc

        self.stdout.write(
            self.style.SUCCESS(
                f"First staff admin '{admin_user.username}' created successfully."
            )
        )

    def _build_database_error_message(self, database_url: str, exc: Exception) -> str:
        message = str(exc)
        base_message = "Database connection failed while seeding the admin."

        if "password authentication failed" in message.lower():
            return (
                f"{base_message} PostgreSQL rejected the username/password in DATABASE_URL. "
                f"Update DATABASE_URL in .env and retry. Current host config: {database_url or 'not set'}"
            )

        return (
            f"{base_message} Check DATABASE_URL and ensure PostgreSQL is running and reachable. "
            f"Details: {message}"
        )
