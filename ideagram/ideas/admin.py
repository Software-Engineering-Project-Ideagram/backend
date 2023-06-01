from django.contrib import admin

from ideagram.ideas.models import Organization, Idea, Classification

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid']
    list_filter = ['name']
    #list_editable = ['name']


class IdeaAdmin(admin.ModelAdmin):
    list_display = ['profile', 'title', 'likes_count', 'views_count']


admin.site.register(Idea, IdeaAdmin)
admin.site.register(Classification)
