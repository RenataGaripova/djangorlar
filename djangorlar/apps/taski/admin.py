# Python modules
from typing import Optional

# Django modules
from django.contrib.admin import ModelAdmin, register
from django.core.handlers.wsgi import WSGIRequest

# Project modules
from .models import Task, UserTask, Project


@register(Project)
class ProjectAdmin(ModelAdmin):
    """
    Project admin configuration class.
    """

    list_display = (
        "id",
        "name",
        "author",
        "created_at"
    )
    list_display_links = (
        "id",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "name",
    )
    ordering = (
        "-updated_at",
    )
    # list_editable = (
    #     "name",
    # )
    list_filter = (
        # "author",
        "updated_at",
    )

    # fields = (
    #     "name",
    #     "author",
    #     "users",
    # )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    filter_horizontal = (
        "users",
    )
    save_on_top = True
    fieldsets = (
        (
            "Project Information",
            {
                "fields": (
                    "name",
                    "author",
                    "users",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            }
        )
    )

    # def get_readonly_fields(self, request: WSGIRequest, obj:
    # Optional[Project] = None) -> Sequence[str]:
    #     """Get dynamically readonly fields."""
    #     if obj:
    #         return self.readonly_fields + ("author", "name", "users")
    #     return self.readonly_fields

    def has_add_permission(self, request: WSGIRequest) -> bool:
        """Disable add permission."""
        return False

    def has_delete_permission(
            self, request: WSGIRequest,
            obj: Optional[Project] = None
    ) -> bool:
        """Disable delete permission."""
        return False

    def has_change_permission(
            self, request: WSGIRequest,
            obj: Optional[Project] = None
    ) -> bool:
        """Disable change permission."""
        return False

    # def has_module_permission(self, request: WSGIRequest) -> bool:
    #     """Disable module permission."""
    #     return False


@register(Task)
class TaskAdmin(ModelAdmin):
    """
    Task admin configuration class.
    """

    list_display = (
        "id", "name", "status", "parent", "project",
    )
    list_display_links = (
        "id",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "name",
        "project",
        "parent",
        "status",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "updated_at",
    )
    list_editable = (
        "status",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    filter_horizontal = (
        "assignees",
    )
    save_on_top = True
    fieldsets = (
        (
            "Task Information",
            {
                "fields": (
                    "name",
                    "description",
                    "parent",
                    "project"
                    "status",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            }
        )
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        """Add permissions."""
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj: Optional[Project] = None):
        """Delete permissions."""
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj: Optional[Project] = None):
        """Change permissions."""
        if request.user.is_superuser:
            return True
        return False


@register(UserTask)
class UserTaskAdmin(ModelAdmin):
    """
    UserTask admin configuration class.
    """

    """
    Task admin configuration class.
    """

    list_display = (
        "id", "task", "user",
    )
    list_display_links = (
        "id",
    )
    list_per_page = 50
    search_fields = (
        "id",
        "task",
        "user",
    )
    ordering = (
        "-updated_at",
    )
    list_filter = (
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "deleted_at",
    )
    save_on_top = True
    fieldsets = (
        (
            "Relationship Information",
            {
                "fields": (
                    "task",
                    "user",
                )
            }
        ),
        (
            "Date and Time Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            }
        )
    )

    def has_add_permission(self, request: WSGIRequest) -> bool:
        """Add permissions."""
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj: Optional[Project] = None):
        """Delete permissions."""
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj: Optional[Project] = None):
        """Change permissions."""
        if request.user.is_superuser:
            return True
        return False
