from django.contrib import admin

# Register your models here.
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "timestamp",
    )
    list_filter = ("user",)
    search_fields = ("user",)


admin.site.register(UserProfile, UserProfileAdmin)
