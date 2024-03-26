from django.contrib import admin

from rabah_dashboard.models import ContactUs


# Register your models here.

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'timestamp')
    search_fields = ['name', 'email', 'message']
    list_filter = ['timestamp']
