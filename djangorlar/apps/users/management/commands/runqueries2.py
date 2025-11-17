# Python modules
from datetime import date, datetime
from typing import Any

# Django modules
from django.core.management.base import BaseCommand
from django.db.models import (
    Q,
    Count,
    Avg,
    Value,
    CharField,
    F,
    Case,
    When,
    Sum,
    ExpressionWrapper,
    IntegerField,
    BooleanField
)
from django.db.models.functions import Now

# Project modules
from ....users.models import CustomUser


class Command(BaseCommand):
    help = "Runs ORM queries on User model."

    def __run_queries2(self) -> None:
        """Main command, to perform queries."""

        may_users = CustomUser.objects.filter(
            birth_date__month=5,
        )
        may_users_count = may_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total users born in may: {may_users_count}\n"
            )
        )

        managers_users = CustomUser.objects.filter(
            Q(role="1") & Q(salary__gt=400000)
        )
        managers_users_count = managers_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total managers with salary greater than 400000: "
            f"{managers_users_count}\n"
            )
        )

        employee_or_hr = CustomUser.objects.filter(
            Q(role="2") | Q(department="HR")
        )
        employee_or_hr_count = employee_or_hr.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total employees or hrs: "
            f"{employee_or_hr_count}\n"
            )
        )

        active_users_by_cities = CustomUser.objects.filter(
            is_active=True).values(
            "city").annotate(total=Count("id"))
        self.stdout.write(self.style.SUCCESS(
            f"Active users in each city: {active_users_by_cities}\n"
            )
        )

        earliest_users = CustomUser.objects.order_by("date_joined")[:10]
        self.stdout.write(self.style.SUCCESS(
            f"10 earliest users: {earliest_users}\n"
            )
        )

        a_city_300k_salary_users = CustomUser.objects.filter(
            Q(city__startswith="A") & Q(salary__gt=300000)
        )
        a_city_300k_salary_users_count = a_city_300k_salary_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users with city starts with 'A' and salary is greater than 300k"
            f" :{a_city_300k_salary_users_count}\n"
            )
        )

        no_department_users = CustomUser.objects.filter(
            Q(department__isnull=True) | Q(department="")
        )
        no_department_users_count = no_department_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users with no department"
            f" :{no_department_users_count}\n"
            )
        )

        countries_stats = CustomUser.objects.values(
            "country").annotate(
                total_users=Count("id"),
                avg_salary=Avg("salary"),
            )
        self.stdout.write(self.style.SUCCESS(
            f"Countries statistics :{countries_stats}\n"
            )
        )

        staff_users = CustomUser.objects.filter(
            is_staff=True,
        ).order_by("-last_login")
        staff_users_count = staff_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Staff users count:{staff_users_count}\n"
            )
        )

        no_example_mail_users = CustomUser.objects.exclude(
            email__icontains="@example.com"
        )
        no_example_mail_users_count = no_example_mail_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users without @example.com mail:{no_example_mail_users_count}\n"
            )
        )

        avg_salary = CustomUser.objects.all().aggregate(Avg("salary"))
        sal_more_than_avg_users = CustomUser.objects.filter(
            salary__gt=avg_salary['salary__avg'],
        )
        sal_more_than_avg_users_count = sal_more_than_avg_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users with salary > avg:{sal_more_than_avg_users_count}\n"
            )
        )

        common_emails = CustomUser.objects.values("email").annotate(
            total=Count("id")).filter(total__gt=1)
        self.stdout.write(self.style.SUCCESS(
            f"Common emails:{common_emails}\n"
            )
        )

        salary_levels_users = CustomUser.objects.annotate(
            salary_level=Case(
                    When(salary__lt=300000, then=Value("Low")),
                    When(
                        Q(salary__gte=300000) & Q(salary__lt=700000),
                        then=Value("Medium")
                    ),
                    When(salary__gte=700000, then=Value("High")),
                    default=Value("Medium"),
                    output_field=CharField(),
                )
            ).order_by("salary_level")
        self.stdout.write(self.style.SUCCESS(
            f"Salary level orderd users:{salary_levels_users}\n"
            )
        )

        this_year_joined = CustomUser.objects.filter(
            date_joined__year=date.today().year,
        )
        this_year_joined_count = this_year_joined.count()
        self.stdout.write(self.style.SUCCESS(
            f"This year joined: {this_year_joined_count}\n"
            )
        )

        salaries_per_department = CustomUser.objects.values(
            "department").annotate(
            total_salary=Sum("salary"),
        )
        self.stdout.write(self.style.SUCCESS(
            f"Salaries by departments: {salaries_per_department}\n"
            )
        )

        it_never_logged_in = CustomUser.objects.filter(
            Q(department="IT") & Q(last_login__isnull=True),
        )
        it_never_logged_in_count = it_never_logged_in.count()
        self.stdout.write(self.style.SUCCESS(
            f"It workers that never logged in: {it_never_logged_in_count}\n"
            )
        )

        incomplete_profiles = CustomUser.objects.filter(
            Q(country="Kazakhstan") & (Q(city__isnull=True) | Q(city="")),
        )
        incomplete_profiles_count = incomplete_profiles.count()
        self.stdout.write(self.style.SUCCESS(
            f"Total incomplete profiles: {incomplete_profiles_count}\n"
            )
        )

        birth_date_before_1990 = CustomUser.objects.filter(
            Q(birth_date__lt=date(year=1990, month=1, day=1))
            & Q(salary__isnull=False),
        )
        birth_date_before_1990_count = birth_date_before_1990.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users born before 1990.01.01: {birth_date_before_1990_count}\n"
            )
        )

        days_since_join = CustomUser.objects.annotate(
            days_since_join=ExpressionWrapper(
                Now() - F("date_joined"),
                output_field=IntegerField()
            ),
        )
        days_since_join = days_since_join.values("email", "days_since_join")
        self.stdout.write(self.style.SUCCESS(
            f"Days since joined: {birth_date_before_1990_count}\n"
            )
        )

        gmail_sales_350k_sal_users = CustomUser.objects.filter(
            Q(email__iendswith="@gmail.com") &
            Q(department="SLS") &
            Q(salary__gt=350000)
        )
        gmail_sales_350k_sal_users_count = gmail_sales_350k_sal_users.count()
        self.stdout.write(self.style.SUCCESS(
            f"Users whose department is 'Sales' and whose email ends with "
            f" @gmail.com and salary > 350000: "
            f" {gmail_sales_350k_sal_users_count}\n"
            )
        )

        order_by_country_salary = CustomUser.objects.order_by(
            "country", "-salary").values("email", "country", "salary")
        self.stdout.write(self.style.SUCCESS(
            f"Sorted users (by country, salary): {order_by_country_salary}\n"
            )
        )

        group_by_role_users = CustomUser.objects.values(
            "role").annotate(total_per_role=Count("id")).filter(
                total_per_role__gt=100,
            )
        self.stdout.write(self.style.SUCCESS(
            f"Group by roles: {group_by_role_users}\n"
            )
        )

        inconsistent_dates_check = CustomUser.objects.filter(
            last_login__lt=F("date_joined"),
        )
        self.stdout.write(self.style.SUCCESS(
            f"Users with last_login > their date_joined: "
            f" {inconsistent_dates_check}\n"
            )
        )

        is_senior_annotation = CustomUser.objects.annotate(
            is_senior=Case(
                When(
                    birth_date__lte=date(year=1985, month=1, day=1),
                    then=Value(True)
                    ),
                When(
                    birth_date__gt=date(year=1985, month=1, day=1),
                    then=Value(False)
                    ),
                default=Value(False),
                output_field=BooleanField(),
            )
        )
        self.stdout.write(self.style.SUCCESS(
            f"Is senior annotation results: {is_senior_annotation.values(
                "email", "is_senior")}\n"
            )
        )

        departments_sorted_by_avg_salary = CustomUser.objects.values(
            "department").annotate(
            total_users=Count("id"),
            avg_salary=Avg("salary"),
        ).filter(total_users__gt=20).order_by("-avg_salary")
        self.stdout.write(self.style.SUCCESS(
            f"Departments sorted by avg salaries: "
            f" {departments_sorted_by_avg_salary}\n"
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        time_now: datetime = datetime.now()
        self.__run_queries2()
        self.stdout.write(
            self.style.SUCCESS(
                f"The process of running 25 queries: "
                f"{(datetime.now() - time_now).total_seconds()}\n"
            )
        )
