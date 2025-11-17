# Python modules
from faker import Faker
from random import choice, uniform
from typing import Any
from datetime import datetime

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

# Project modules
from ....users.models import CustomUser


fake = Faker()


class Command(BaseCommand):
    help = "Generates test data for project model."

    def __generate_users(self, user_count: int = 10000) -> None:
        """Generates fake users."""

        USER_PASSWORD = make_password("qwerty")
        created_users: list[CustomUser] = []

        i: int

        for i in range(user_count):
            email = fake.unique.email()
            phone = fake.phone_number()
            first_name = fake.first_name()
            last_name = fake.last_name()
            country = fake.country()
            city = fake.city()
            department = choice(CustomUser.DEPARTMENT_CHOICES)[0]
            birth_date = fake.date_of_birth(maximum_age=50, minimum_age=21)
            salary = uniform(50000.00, 500000.00)
            role = choice(CustomUser.ROLES_CHOICES)[0]

            created_users.append(
                CustomUser(
                    email=email,
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    city=city,
                    department=department,
                    birth_date=birth_date,
                    salary=salary,
                    role=role,
                    password=USER_PASSWORD,
                )
            )

        CustomUser.objects.bulk_create(
            created_users,
            batch_size=1000,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {user_count} users."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        time_now: datetime = datetime.now()
        self.__generate_users(user_count=10000)
        self.stdout.write(
            self.style.SUCCESS(
                f"The process of generating data has taken: "
                f"{(datetime.now() - time_now).total_seconds()}"
            )
        )
