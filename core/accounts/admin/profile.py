from django.contrib import admin
from accounts.models.profile import Profile, Skills


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "username", "email", "created_time")
    list_filter = (
        "user",
        "username",
        "email",
        "created_time",
    )
    fieldsets = [
        (
            "User",
            {
                "fields": ("user",),
            },
        ),
        (
            "Information",
            {
                "fields": ("username", "email", "age", "bio"),
            },
        ),
        (
            "Skills",
            {
                "fields": ("skills",),
            },
        ),
    ]

    add_fieldsets = [
        (
            "Add user profile",
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                ],
            },
        ),

    ]
    search_fields = (
        "username",
        "email",
    )
    ordering = (
        "created_time",
        "updated_time",
    )
    readonly_fields = (
        "created_time",
        "updated_time",
    )


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    """Admin View for Skills"""

    list_display = ("name",)
    search_fields = ("name",)
