from django.contrib import admin
from ideagram.profiles.models import ProfileLinks, Following


class ProfileLinksAdmin(admin.ModelAdmin):
    list_display = ['profile', 'type', 'link']


class FollowingAdmin(admin.ModelAdmin):
    list_display = ['profile', 'profile_following']




admin.site.register(ProfileLinks, ProfileLinksAdmin)
admin.site.register(Following, FollowingAdmin)
