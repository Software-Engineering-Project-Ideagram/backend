from django.contrib import admin

from ideagram.ideas.models import Organization

# Register your models here.
@admin.register(Organization)
class ForbiddenWordAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid']
    list_filter = ['name']
    #list_editable = ['name']


