from django.contrib import admin

# Register your models here.
from .models import Contribution,ContributionType


admin.site.register(Contribution)
admin.site.register(ContributionType)