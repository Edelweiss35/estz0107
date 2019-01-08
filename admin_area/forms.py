from contact.models import ContactAdminResponse, ContactExpertResponse, ExpertResponse, ContactExpert

from django.forms import ModelForm, Textarea

from django.core.mail import send_mail, EmailMessage

from django.conf import settings
from django.template.loader import render_to_string

# from django.forms.models import inlineformset_factory

from django.forms.models import BaseInlineFormSet
import os

class ExpertResponseFormset(BaseInlineFormSet):
    pass


# ExpertResponseFormSet = inlineformset_factory(ExpertResponse,
#                                               ContactExpert,
#                                               formset=ExpertResponseFormset,
#                                               extra=3,
#                                               fields=('expert',))


class ContactAdminResponseForm(ModelForm):

    # send emails to admin and user
    def send_emails(self):
        # try to send mail

        # msg_plain = render_to_string('contact/contact_admin_accepted.txt', {'username': self.cleaned_data['name']})

        if not self.instance:
            raise RuntimeError('this function must be run after form save')

        if self.instance.type == 'R':  # response
            # response
            email = EmailMessage(
                'Ответ на Ваше обращение на сайте estz.su',
                self.instance.message,
                settings.EMAIL_FROM,
                [self.instance.email, ],
                # reply_to=['another@example.com'],
                # headers={'Message-ID': 'foo'},
            )

            if self.instance.attach:
                # email.attach(os.path.basename(self.instance.attach.name), self.instance.attach.read(), self.instance.attach.content_type)
                email.attach_file(self.instance.attach.path)

            email.send()

        elif self.instance.type == 'F':  # forward
            # forward
            try:
                email = EmailMessage(
                    'Обращение, пересланное с estz.su',
                    self.instance.message,
                    settings.EMAIL_FROM,
                    [self.instance.email, ],
                    reply_to=[self.instance.contactadmin.email],  # user email
                    # headers={'Message-ID': 'foo'},
                )
                if self.instance.contactadmin.file:
                    # email.attach(os.path.basename(self.instance.contactadmin.file.name), self.instance.contactadmin.file.read(), self.instance.contactadmin.file.content_type)
                    email.attach_file(self.instance.attach.path)
                # if self.instance.attach:
                #     email.attach(self.instance.attach, self.instance.attach.read(), self.instance.attach.content_type)

                email.send()

                # response to user
                email = EmailMessage(
                    'Ваше обращение на сайте estz.su было переслано.',
                    self.instance.message,
                    settings.EMAIL_FROM,
                    [self.instance.contactadmin.email, ],
                )

                if self.instance.attach:
                    email.attach_file(self.instance.attach.path)
                    # email.attach(self.instance.attach, self.instance.attach.read(), self.instance.attach.content_type)

                email.send()

            except Exception as e:
                pass

    class Meta:
        model = ContactAdminResponse
        fields = ['email', 'message', 'attach']
        widgets = {
            'message': Textarea(attrs={'rows': 3}),
        }


class ContactExpertResponseForm(ModelForm):

    # send emails to admin and user
    def send_emails(self):
        email = EmailMessage(
            'Ответ на Ваше обращение к эксперту сайте estz.su',
            self.instance.message,
            settings.EMAIL_FROM,
            [self.instance.email, ],
            # reply_to=['another@example.com'],
            # headers={'Message-ID': 'foo'},
        )

        if self.instance.attach:
            # email.attach(os.path.basename(self.instance.attach.name), self.instance.attach.read(), self.instance.attach.content_type)
            email.attach_file(self.instance.attach.path)

        email.send()


    class Meta:
        model = ContactExpertResponse
        fields = ['email', 'message', 'attach']
        widgets = {
            'message': Textarea(attrs={'rows': 3}),
        }


# class ExpertResponseForm(ModelForm):
#     class Meta:
#         model = ContactExpertResponse
#         fields = ['email', 'message', 'attach']
#         widgets = {
#             'message': Textarea(attrs={'rows': 3}),
#         }
