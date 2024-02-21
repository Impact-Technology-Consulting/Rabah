from django.contrib import admin
from .models import Organisation, Group


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'timestamp')
    search_fields = ('name',)
    list_filter = ('owner', 'timestamp')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'timestamp')
    search_fields = ('name', 'organisation__name')
    list_filter = ('organisation', 'timestamp')
    readonly_fields = ('imageURL',)

    def save_model(self, request, obj, form, change):
        """Override the save_model method to handle image file saving."""
        super().save_model(request, obj, form, change)
        if 'image' in form.cleaned_data:
            obj.image = form.cleaned_data['image']
            obj.save()
