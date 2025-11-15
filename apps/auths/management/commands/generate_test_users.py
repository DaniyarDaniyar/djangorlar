# Pyrhon modules
from typing import Any
from random import choice, choices, randint
from datetime import date, datetime
from faker import Faker

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

# Project modules
from apps.auths.models import CustomUser

class Command(BaseCommand):
    """Django management command to generate test users"""

    help = "Generate test users for development and testing purposes"

    DEPARTMENTS = (
        "IT",
        "HR",
        "Finance",
        "Sales",
        "Marketing",
    )
    ROLE_CHOICES = list(CustomUser.ROLE_CHOICES.keys())

    def __generate_test_users(self, total_count: int=10000) -> None:
        """Generate test users"""
        faker: Faker = Faker()
        USER_PASSWORD = make_password("12345")
        batch_size: int = 1000

        users_before: int = CustomUser.objects.count()
        created_users: int = 0

        for batch_num in range(total_count // batch_size):
            batch_users: list[CustomUser] = []

            for _ in range(batch_size):
                first_name: str = faker.first_name()
                last_name: str = faker.last_name()
                email: str = faker.unique.email()
                username: str = faker.unique.user_name()

                user = CustomUser(
                    email=email,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=USER_PASSWORD,
                    is_active=True,
                    is_staff=choice([True, False]),
                    role=choice(self.ROLE_CHOICES),
                    department=choice(self.DEPARTMENTS),
                    birth_date=faker.date_between_dates(
                        date_start=date(1975, 1, 1),
                        date_end=date(2005, 12, 31),
                    ),
                    salary=randint(200000, 1500000),
                    city=faker.city(),
                    country=faker.country(),
                    phone_number=faker.phone_number(),
                )

                batch_users.append(user)

            CustomUser.objects.bulk_create(batch_users, ignore_conflicts=True)
            created_users += len(batch_users)
            self.stdout.write(
                self.style.NOTICE(
                    f"Batch {batch_num + 1}: Created {len(batch_users)} users."
                )
            )

        users_after: int = CustomUser.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Total users before: {users_before}, after: {users_after}. "
                f"Total created: {users_after - users_before}."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Handle the command to generate test users"""
        
        start_time: datetime = datetime.now()

        self.__generate_test_users()

        self.stdout.write(
            self.style.SUCCESS(
                f"Test users generated successfully in {datetime.now() - start_time}"
            )
        )