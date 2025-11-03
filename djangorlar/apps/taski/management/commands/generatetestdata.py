# Python modules
from random import choice, choices

# Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet

from apps.taski.models import Project, Task, UserTask


class Command(BaseCommand):
    help = "Generates test data for project model."
    NAME_MAX_LEN = 200
    STATUS_TODO = 1
    STATUS_TODO_LABEL = "To Do"
    STATUS_IN_PROGRESS = 2
    STATUS_IN_PROGRESS_LABEL = "In Progress"
    STATUS_DONE = 3
    STATUS_DONE_LABEL = "Done"

    STATUS_CHOICES = {
        STATUS_TODO: STATUS_TODO_LABEL,
        STATUS_IN_PROGRESS: STATUS_IN_PROGRESS_LABEL,
        STATUS_DONE: STATUS_DONE_LABEL,
    }

    EMAIL_DOMAINS = (
        "example.com",
        "test.com",
        "sample.org",
        "demo.net",
        "mail.com",
    )
    SOME_WORDS = (
        "lorem",
        "ipsum",
        "dolor",
        "sit",
        "amet",
        "consectetur",
        "adipiscing",
        "elit",
        "sed",
        "do",
        "eiusmod",
        "tempor",
        "incididunt",
        "ut",
        "labore",
        "et",
        "dolore",
        "magna",
        "aliqua",
    )

    def __generate_users(self, user_count: int = 20) -> None:
        """Generates users for testing purposes."""

        USER_PASSWORD = make_password("abcdef")
        created_users: list[User] = []
        user_before_cnt = User.objects.count()
        i: int
        for i in range(user_count):
            username: str = f"user {i}"
            email: str = f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_users.append(
                User(
                    username=username,
                    email=email,
                    password=USER_PASSWORD,
                )
            )
        User.objects.bulk_create(
            created_users,
            ignore_conflicts=True,
        )
        user_after_cnt = User.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {user_after_cnt - user_before_cnt} users."
            )
        )

    def __generate_projects(self, project_count: int = 20) -> None:
        """Generates users for testing purposes."""

        created_projects: list[Project] = []
        projects_before_cnt = Project.objects.count()
        test_users: QuerySet[User] = User.objects.all()
        i: int
        for i in range(project_count):
            name: str = f"project {i}"
            author: User = choice(test_users)
            created_projects.append(
                Project(
                    name=name,
                    author=author,
                )
            )
        Project.objects.bulk_create(
            created_projects,
            ignore_conflicts=True,
        )

        project: Project

        for project in Project.objects.all():
            project.users.add(*choices(test_users, k=5))

        projects_after_cnt = Project.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {projects_after_cnt - projects_before_cnt} users."
            )
        )

    def __generate_tasks(self, task_count: int = 20) -> None:
        """Generates users for testing purposes."""

        created_tasks: list[Task] = []
        created_usertasks: list[UserTask] = 0
        tasks_before_cnt = Task.objects.count()
        test_users: QuerySet[User] = User.objects.all()
        existed_projects: QuerySet[Project] = Project.objects.all()
        i: int
        for i in range(task_count):
            name: str = f"task {i}"
            description: str = f"description for task: {i}"
            project = choice(existed_projects)
            created_tasks.append(
                Task(
                    name=name,
                    description=description,
                    status=choice(self.STATUS_CHOICES),
                    project=project,

                )
            )
        Task.objects.bulk_create(
            created_tasks,
            ignore_conflicts=True,
        )

        task: Task

        for task in Task.objects.all():
            chosen_users = choices(test_users, k=5)
            user: User
            for user in chosen_users:
                task.assignees.add(user)
                UserTask()
            task.assignees.add(*choices(test_users, k=5))
            created_usertasks.append(
                UserTask(
                    task=task,
                    user=user,
                )
            )
        tasks_after_cnt = Task.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {tasks_after_cnt - tasks_before_cnt} users."
            )
        )
