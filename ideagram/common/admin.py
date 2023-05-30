from django.contrib import admin

from ideagram.common.models import Address
from ideagram.common.models import ForbiddenWord



# Register your models here.
@admin.register(ForbiddenWord)
class ForbiddenWordAdmin(admin.ModelAdmin):
    list_display = ['word']
    list_filter = ['word']

admin.register(Address)
