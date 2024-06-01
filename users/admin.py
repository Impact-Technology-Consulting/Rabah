from django.contrib import admin

# Register your models here.
from .models import UserProfile, User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "timestamp",
    )
    list_filter = ("user",)
    search_fields = ("user",)


admin.site.register(UserProfile, UserProfileAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "mobile",
        "is_active",
        "is_staff",
        "verified",
        "is_billing_verified",
        "date_joined",
        "timestamp",
    )
    list_filter = ("first_name","email","last_name",)
    search_fields = ("first_name","email","last_name",)


admin.site.register(User, UserAdmin)
