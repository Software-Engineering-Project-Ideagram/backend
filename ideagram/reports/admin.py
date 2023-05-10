from django.contrib import admin

from ideagram.reports.models import ProfileReport
from ideagram.profiles.models import Profile
from ideagram.users.models import BaseUser


# Register your models here.
@admin.register(ProfileReport)
class ProfileReportAdmin(admin.ModelAdmin):
    list_display = ['profile_id', 'reporter_id',  'date', 'report_reasons', 'description', 'is_checked']
    list_editable = ['is_checked']
    list_filter = ['is_checked']
    readonly_fields = ['profile_id', 'reporter_id',  'date', 'report_reasons', 'description']
    actions = ['make_checked']
    @admin.action
    def make_checked(self, request, queryset):
        queryset.update(is_checked=True)

    make_checked.short_description = 'Checked'
@admin.register(Profile)
class ProfileReportAdmin(admin.ModelAdmin):
    pass


@admin.register(BaseUser)
class BaseUserReportAdmin(admin.ModelAdmin):
    pass
