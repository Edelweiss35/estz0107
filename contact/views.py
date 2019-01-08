from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import ContactAdmin, ContactExpert, ExpertResponse
from .forms import ContactAdminForm, ContactExpertForm, ExpertResponseForm


class ContactAdminView(CreateView):

    form_class = ContactAdminForm
    model = ContactAdmin

    def get_success_url(self):
        # return reverse_lazy('contact-admin-success')
        return "/vashe-obrashenie-uspeshno-otpravleno"

    template_name = "contact/contact_admin.html"

    # def get_form(self, form_class=None):
    #     form = super(ContactView, self).get_form(form_class)
    #     form.fields['work_place'].widget = Textarea(attrs={'rows': 6})
    #     return form

    def form_valid(self, form):
        to_return = super().form_valid(form)
        form.send_emails()
        return to_return


class ContactExpertView(CreateView):

    form_class = ContactExpertForm
    model = ContactExpert

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expert_question'] = True
        return context

    def get_success_url(self):
        # return reverse_lazy('contact-admin-success')
        return "/vashe-obrashenie-uspeshno-otpravleno"

    template_name = "contact/contact_admin.html"

    def form_valid(self, form):
        to_return = super().form_valid(form)
        form.send_emails()
        return to_return

import datetime


class ExpertResponseView(UpdateView):
    form_class = ExpertResponseForm
    model = ExpertResponse
    lookup_field = 'uuid'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.object.contact_expert_question
        return context

    def get_success_url(self):
        # return reverse_lazy('contact-admin-success')
        return "/"

    template_name = "contact/expert_response.html"

    def form_valid(self, form):
        self.object.response_date = datetime.datetime.now()
        to_return = super().form_valid(form)
        form.send_emails()
        return to_return
