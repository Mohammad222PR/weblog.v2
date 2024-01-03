from django.contrib import admin
from accounts.models.users import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
        "is_verified",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
    )
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )

    add_fieldsets = [
        (
            "Add user",
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ),
        (
            "permissions",
            {
                "classes": ["wide"],
                "fields": [
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ],
            },
        ),
        (
            "group permissions",
            {
                "classes": ["wide"],
                "fields": [
                    "groups",
                    "user_permissions",
                ],
            },
        ),
    ]




