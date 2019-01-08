from django import forms
from django.contrib import admin


class AdminFileWidget(forms.ClearableFileInput):
    template_name = 'contact/admin/widgets/clearable_file_input.html'


class ContactExpertAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactExpertAdminForm, self).__init__(*args, **kwargs)
        self.fields['work_place'].widget = admin.widgets.AdminTextareaWidget(attrs={'rows': 2, })
        self.fields['file'].widget = AdminFileWidget()

