from django.contrib import admin

from .models import ContactAdmin, ContactAdminStatus, ContactAdminResponse
from .admin_forms import ContactExpertAdminForm


class ContactAdminStatusAdmin(admin.ModelAdmin):
    pass


class ContactAdminResponseAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_datetime', 'update_datetime']


class ContactAdminAdmin(admin.ModelAdmin):

    def status_status(self, obj):
        if not obj.status:
            return '<div style="width:100%%; height:100%%; background-color:orange;">Новое</div>'
        return obj.status

    status_status.allow_tags = True
    readonly_fields = ['creation_datetime', 'update_datetime']
    list_display = ['surname', 'name', 'email', 'phone', 'status_status', 'creation_datetime']


admin.site.register(ContactAdmin, ContactAdminAdmin)
admin.site.register(ContactAdminStatus, ContactAdminStatusAdmin)
admin.site.register(ContactAdminResponse, ContactAdminResponseAdmin)


from django.contrib import admin

from .models import ContactExpert, ContactExpertStatus, ContactExpertResponse, Expert, ExpertResponse


class ContactExpertStatusExpert(admin.ModelAdmin):
    pass


class ExpertAdmin(admin.ModelAdmin):
    pass


class ExpertResponseAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid']


class ContactExpertStatusExpertAdmin(admin.ModelAdmin):
    pass


class ContactExpertResponseExpertAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_datetime', 'update_datetime']


class ContactExpertAdmin(admin.ModelAdmin):
    form = ContactExpertAdminForm

    def status_status(self, obj):
        if not obj.status:
            return '<div style="width:100%%; height:100%%; background-color:orange;">Новое</div>'
        return obj.status

    status_status.allow_tags = True
    readonly_fields = ['creation_datetime', 'update_datetime']
    list_display = ['surname', 'name', 'email', 'phone', 'status_status', 'creation_datetime']


admin.site.register(ContactExpert, ContactExpertAdmin)
admin.site.register(ContactExpertStatus, ContactExpertStatusExpertAdmin)
admin.site.register(ContactExpertResponse, ContactExpertResponseExpertAdmin)

admin.site.register(Expert, ExpertAdmin)
admin.site.register(ExpertResponse, ExpertResponseAdmin)
