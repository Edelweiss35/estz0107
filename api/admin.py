from django.contrib import admin
from .models import *


# Register your models here.
class UserSubcriberNewsAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')

    def has_add_permission(self, request):
        return False

admin.site.register(UserSubcriberNews, UserSubcriberNewsAdmin)