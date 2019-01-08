from django.core import serializers
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from contact.models import ContactAdmin, ContactExpert

from django.http import Http404
from django.http import JsonResponse

from django.shortcuts import redirect

from contact.models import ContactAdminStatus
from contact.models import ContactExpertStatus, Expert, ExpertResponse

from .forms import ContactAdminResponseForm, ContactExpertResponseForm

from django.db.models import Value, CharField

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AdminIndexView(TemplateView):
    template_name = 'admin_area/base.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AdminContactListView(ListView):
    template_name = 'admin_area/contactadmin_list.html'

    model = ContactAdmin
    paginate_by = 20  # TODO move to settings
    ordering = ['-creation_datetime']
    return_fields = ('id', 'surname', 'name', 'email', 'status__title', 'status',
                                              'creation_datetime', 'contact_choice', 'phone')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['data'] = context['object_list'].\
            prefetch_related('status').values(*self.return_fields)

        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class AdminContactDetailView(DetailView):
    template_name = 'admin_area/contactadmin_detail.html'

    model = ContactAdmin
    response_form = ContactAdminResponseForm

    def get_context_data(self, contact_response_form=None, initial_addition_to_form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['fields'] = [(field.name, getattr(context['object'], field.name)) for field in self.model._meta.get_fields()]

        if contact_response_form:
            context['contact_response_form'] = contact_response_form
        else:
            if context['object'].response:
                context['contact_response_form'] = self.response_form(instance=context['object'].response,)
            else:
                initial_data = {'email': context['object'].email}
                if initial_addition_to_form:
                    initial_data.update(initial_addition_to_form)
                context['contact_response_form'] = self.response_form(initial=initial_data)\
                    # ,
                    #                                                                  'contact_admin': context['object']})
        return context

    def post(self, request, *args, **kwargs):
        contact_response_form = self.response_form(request.POST, request.FILES)
        if contact_response_form.is_valid():
            # send emails
            response_admin = contact_response_form.save()
            # response_admin
            ca = self.model.objects.get(pk=int(kwargs.get('pk', 0)))
            if response_admin.email == ca.email:
                # response
                response_admin.type = 'R'
                ca.status_id = 3
            else:
                # forward
                response_admin.type = 'F'
                ca.status_id = 4
            ca.response = response_admin
            ca.save()
            contact_response_form.send_emails()

            from django.http import HttpResponseRedirect
            from django.urls import reverse

            return HttpResponseRedirect(reverse('admin-contact-response-success'))
        kwargs['contact_response_form'] = contact_response_form
        return self.get(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        contact_response_form = None
        if 'contact_response_form' in kwargs:
            contact_response_form = kwargs['contact_response_form']

        context = self.get_context_data(contact_response_form=contact_response_form, object=self.object)
        return self.render_to_response(context)


class AdminContactExpertListView(AdminContactListView):
    model = ContactExpert
    template_name = 'admin_area/contactexpert_list.html'
    return_fields = ('id', 'surname', 'name', 'email', 'status__title', 'status',
                     'creation_datetime', 'phone')


class AdminContactExpertDetailView(AdminContactDetailView):
    def get_context_data(self, **kwargs):
        default_message = """Здравствуйте! Направляю ответ эксперта(ов) на Ваше обращение, принятое на сайте ЕСТЗ. 
Ответ смотрите во вложении. 
С Уважением, Генеральный директор ООО "ЕСТЗ" Чернышов А.Е.
тел. +7 (926) 834-69-43"""
        context = super().get_context_data(initial_addition_to_form={'message': default_message}, **kwargs)
        # Add in a QuerySet of all the books
        context['experts'] = Expert.objects.all()
        context['question_id'] = self.object.id
        return context

    model = ContactExpert
    response_form = ContactExpertResponseForm
    template_name = 'admin_area/contactexpert_detail.html'


    def post(self, request, *args, **kwargs):
        contact_expert_response_form = self.response_form(request.POST, request.FILES)
        if contact_expert_response_form.is_valid():
            # send emails
            response_admin = contact_expert_response_form.save()
            # response_expert
            ca = self.model.objects.get(pk=int(kwargs.get('pk', 0)))
            ca.status_id = 3
            ca.response = response_admin
            ca.save()
            contact_expert_response_form.send_emails()

            from django.http import HttpResponseRedirect
            from django.urls import reverse

            return HttpResponseRedirect(reverse('admin-contact-response-success'))
        kwargs['contact_response_form'] = contact_expert_response_form
        return self.get(self, request, *args, **kwargs)



# TODO unify it
@user_passes_test(lambda u: u.is_superuser)
def change_status(request):
    if not request.is_ajax():
        raise Http404("Page not found")

    status_pk = request.POST.get('status_pk', None)
    contact_admin_pk = request.POST.get('contact_admin_pk', None)

    try:
        ct = ContactAdmin.objects.get(pk=contact_admin_pk)
        cts = ContactAdminStatus.objects.get(pk=status_pk)
    except (ContactAdmin.DoesNotExist, ContactAdminStatus.DoesNotExist):
        raise Http404()

    ct.status = cts
    ct.save()

    return JsonResponse({'response': 'success'})


@user_passes_test(lambda u: u.is_superuser)
def change_contactexpert_status(request):
    if not request.is_ajax():
        raise Http404("Page not found")

    status_pk = request.POST.get('status_pk', None)
    contact_admin_pk = request.POST.get('contact_admin_pk', None)

    try:
        ct = ContactExpert.objects.get(pk=contact_admin_pk)
        cts = ContactExpertStatus.objects.get(pk=status_pk)
    except (ContactAdmin.DoesNotExist, ContactAdminStatus.DoesNotExist):
        raise Http404()

    ct.status = cts
    ct.save()

    return JsonResponse({'response': 'success'})


from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


@user_passes_test(lambda u: u.is_superuser)
def send_to_experts(request, pk):
    experts = request.POST.getlist('experts')

    for expert_id in experts:
        expert = Expert.objects.get(pk=expert_id)
        contact_expert_question = ContactExpert.objects.get(pk=pk)
        contact_expert_question.status_id = 2
        contact_expert_question.save()
        new_response = ExpertResponse.objects.create(expert=expert, contact_expert_question=contact_expert_question)

        # send email to expert
        send_mail(
            'Поступило обращение к эксперту на сайте estz.su',
            'Администратор направил Вам обращение, оставленное заявителем {} на рассмотрение эксперту на сайте estz.su. '
            'Для того, чтобы прочитать запрос и дать ответ перейдите на страницу: http://estz.su{}'.
            format(contact_expert_question.full_name, reverse('response-expert-to-client', kwargs={'slug': str(new_response.uuid)})),
            settings.EMAIL_FROM,
            [expert.email, ],
        )

    return redirect('admin-contact-expert-list')
