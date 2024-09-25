from .models import User
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "business_name", "phone_number", "is_verified")
    readonly_fields = ("created_at",)


admin.site.register(User, UserAdmin)