import core.models as core_models
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.site_header = "LegioFit"
admin.site.site_title = "LegioFit"
admin.site.index_title = "Welcome Admin"
admin.site.unregister(Group)


@admin.action(description="Inactivate selected Users")
def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Activate selected Users")
def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Soft Delete selected Users")
def soft_delete(modeladmin, request, queryset):
    queryset.update(is_deleted=True)


@admin.register(core_models.User)
class UserAdmin(BaseUserAdmin):
    filter_horizontal = ["groups", "user_permissions"]
    list_display = [
        "id",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = ["email", "first_name", "last_name", "id"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    fieldsets = [
        ("Account", {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "last_login",
                )
            },
        ),
        (
            "Permissions/Status",
            {"fields": ("is_staff", "is_superuser", "is_active")},
        ),
        (
            "Soft/Logical Deletion",
            {"fields": ["is_deleted"]},
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    ]
    actions = [make_inactive, make_active]
    ordering = ["email"]
    per_page = 20
