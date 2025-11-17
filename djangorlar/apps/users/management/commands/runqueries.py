# Python modules
from datetime import date, timedelta, datetime
from typing import Any

# Django modules
from django.core.management.base import BaseCommand
from django.db.models import Q, Count, Avg, Min, Max, Value, CharField, F
from django.db.models.functions import Concat

# Project modules
from ....users.models import CustomUser


class Command(BaseCommand):
    help = "Runs ORM queries on User model."

    def __run_queries(self) -> None:
        """Main command, to perform queries."""

        active_users = CustomUser.objects.filter(
            is_active=True,
        )
        active_users_count = active_users.count()
        self.stdout.write(self.style.SUCCESS(
                f"Total active users: {active_users_count}\n"
            )
        )

        gmail_users = CustomUser.objects.filter(
            email__endswith="@gmail.com"
        )
        gmail_users_count = gmail_users.count()
        self.stdout.write(self.style.SUCCESS(
                f"Total gmail users: {gmail_users_count}\n"
            )
        )

        almaty_users = CustomUser.objects.filter(
            city="Almaty"
        )
        almaty_users_count = almaty_users.count()
        self.stdout.write(self.style.SUCCESS(
                f"Total gmail users: {almaty_users_count}\n"
            )
        )
        non_almaty_users = CustomUser.objects.exclude(
            city="Almaty"
        )
        non_almaty_usersalmaty_users_count = non_almaty_users.count()
        self.stdout.write(self.style.SUCCESS(
                f"Total gmail users: {non_almaty_usersalmaty_users_count}\n"
            )
        )

        salary_50k_gt_users = CustomUser.objects.filter(
            salary__gt=50000,
        )
        salary_50k_gt_users_count = salary_50k_gt_users.count()
        self.stdout.write(self.style.SUCCESS(
                f"Total >50000 salary users: {salary_50k_gt_users_count}\n"
            )
        )

        it_kz_users = CustomUser.objects.filter(
            country="Kazakhstan",
            department="IT",
        )
        it_kz_users_count = it_kz_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total it_kz_users_count users: {it_kz_users_count}\n"
            )
        )

        null_bd_users = CustomUser.objects.filter(
            birth_date__isnull=True,
        )
        null_bd_users_count = null_bd_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total null_bd_users_count users: {null_bd_users_count}\n"
            )
        )

        a_name_users = CustomUser.objects.filter(
            first_name__istartswith="A",
        )
        a_name_users_count = a_name_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total null_bd_users_count users: {a_name_users_count}\n"
            )
        )

        total_users_count = CustomUser.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total users: {total_users_count}\n"
            )
        )

        first_20 = CustomUser.objects.order_by(
            "-date_joined",
        )[20:]
        self.stdout.write(self.style.SUCCESS(
            f"First 20 users: {first_20}\n"
            )
        )

        cities = CustomUser.objects.values_list("city", flat=True).distinct()
        self.stdout.write(self.style.SUCCESS(
            f"User's cities: {cities}\n"
            )
        )

        last_7_days_users = CustomUser.objects.filter(
            last_login=date.today()-timedelta(days=7),
        )
        self.stdout.write(self.style.SUCCESS(
            f"Users logged in during the last 7 days: {last_7_days_users}\n"
            )
        )

        bek_users = CustomUser.objects.filter(
            Q(first_name__icontains="bek") | Q(last_name__icontains="bek")
        )
        bek_users_count = bek_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users with bek in full name : {bek_users_count}\n"
            )
        )

        salary_between_300k_700k = CustomUser.objects.filter(
            Q(salary__gte=300000) & Q(salary__lte=700000),
        )
        salary_between_300k_700k_count = salary_between_300k_700k.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users with salary "
            f"between 300000 and 700000: {salary_between_300k_700k_count}\n"
            )
        )

        it_hr_fnc_users = CustomUser.objects.filter(
            Q(department="IT") | Q(department="IT") | Q(department="FNC"),
        )
        it_hr_fnc_users_count = it_hr_fnc_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total it_hr_fnc_users: {it_hr_fnc_users_count}\n"
            )
        )

        department_groups = CustomUser.objects.values(
            "department").annotate(total=Count("id"))
        self.stdout.write(self.style.SUCCESS(
            f"Departments info: {department_groups}\n"
            )
        )

        department_groups_order_desc = CustomUser.objects.values(
            "department").annotate(total=Count("id")).order_by("-total")
        self.stdout.write(self.style.SUCCESS(
            f"Departments ordered info: {department_groups_order_desc}\n"
            )
        )

        top_cities = department_groups_order_desc = CustomUser.objects.values(
            "city").annotate(total=Count("id")).order_by("-total")[:5]
        self.stdout.write(self.style.SUCCESS(
            f"Top cities: {top_cities}\n"
            )
        )

        never_logged_in = CustomUser.objects.filter(
            last_login__isnull=True,
        )
        self.stdout.write(self.style.SUCCESS(
            f"Never logged in: {never_logged_in}\n"
            )
        )

        avg_salary = CustomUser.objects.all().aggregate(Avg("salary"))
        self.stdout.write(self.style.SUCCESS(
            f"Average salary: {avg_salary}\n"
            )
        )

        min_salary = CustomUser.objects.all().aggregate(Min("salary"))
        self.stdout.write(self.style.SUCCESS(
            f"Min salary: {min_salary}\n"
            )
        )

        max_salary = CustomUser.objects.all().aggregate(Max("salary"))
        self.stdout.write(self.style.SUCCESS(
            f"Max salary: {max_salary}\n"
            )
        )

        phone_plus_7_users = CustomUser.objects.filter(
            phone__icontains="+7",
        )
        phone_plus_7_users_count = phone_plus_7_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total users with phones "
            f"containing +7: {phone_plus_7_users_count}\n"
            )
        )

        full_names = CustomUser.objects.annotate(
            full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
                output_field=CharField())
            )
        self.stdout.write(self.style.SUCCESS(
            f"Full names: {full_names}\n"
            )
        )

        birth_years = CustomUser.objects.annotate(
            birth_year=F("birth_date__year"),
        ).order_by("birth_year")
        self.stdout.write(self.style.SUCCESS(
            f"Users sorted by years: {birth_years}\n"
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        time_now: datetime = datetime.now()
        self.__run_queries()
        self.stdout.write(
            self.style.SUCCESS(
                f"The process of running 25 queries: "
                f"{(datetime.now() - time_now).total_seconds()}\n"
            )
        )
