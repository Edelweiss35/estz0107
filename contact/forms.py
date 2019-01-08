from django.forms import ModelForm, Textarea, BooleanField

from django.core.mail import send_mail

from django.conf import settings
from django.template.loader import render_to_string

# from snowpenguin.django.recaptcha2.fields import ReCaptchaField
# from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

from captcha.fields import CaptchaField

from .models import ContactAdmin, ContactExpert, ExpertResponse

from django.urls import reverse

class ContactAdminForm(ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaWidget())
    captcha = CaptchaField()
    personal_data = BooleanField(required=True,
                                 error_messages={'required':
                                                 'Вы должны принять условие обработки персональных данных'},)

    # send emails to admin and user
    def send_emails(self):
        # try to send mail

        if not self.instance:
            raise RuntimeError('this function must be run after form save')

        msg_plain = render_to_string('contact/contact_admin_accepted.txt', {'username': self.instance.full_name,
                                                                            'number': self.instance.id,
                                                                            'datestr': self.instance.creation_datetime.strftime('%d.%m.%Y'),
                                                                            'what': "Ваше обращение на сайте ESTZ принято"})

        try:
            send_mail('Ваше обращение на сайте ESTZ принято на рассмотрение. ',
                      msg_plain,
                      settings.EMAIL_FROM,
                      [self.cleaned_data['email'],],
            )
        except Exception as e:
            pass
            # TODO LOG this

        for admin in settings.ADMINS:
            send_mail(
                'Поступило обращение к администрации на сайте estz.su',
                '{} оставил обращение на рассмотрение администрации на сайте estz.su. http://estz.su{}'.
                format(self.instance.full_name, reverse('admin-contact-detail', args=[self.instance.id,])),
                settings.EMAIL_FROM,
                [admin[1]],
            )


    # def __init__(self, *args, **kwargs):
    #     super(ContactAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ContactAdmin
        fields = ['surname', 'name', 'patronymic', 'phone', 'email', 'post', 'work_place', 'file', 'message',
                  'contact_choice']

        widgets = {
            'message': Textarea(attrs={'rows': 15, }),
            'work_place': Textarea(attrs={'rows': 2, }),
        }


class ContactExpertForm(ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaWidget())
    captcha = CaptchaField()
    personal_data = BooleanField(required=True,
                                 error_messages={'required':
                                                 'Вы должны принять условие обработки персональных данных'},)

    # send emails to admin and user
    def send_emails(self):
        # try to send mail

        if not self.instance:
            raise RuntimeError('this function must be run after form save')

        username = self.instance.name
        if self.instance.patronymic:
            username = "{} {}".format(username, self.instance.patronymic)

        msg_plain = render_to_string('contact/contact_admin_accepted.txt', {'username': username,
                                                                            'number': self.instance.id,
                                                                            'datestr': self.instance.creation_datetime.strftime('%d.%m.%Y'),
                                                                            'what': "Ваш вопрос к экспертам на сайте ESTZ принят"})

        try:
            send_mail('Ваш вопрос к экспертам на сайте ESTZ принят на рассмотрение.',
                      msg_plain,
                      settings.EMAIL_FROM,
                      [self.cleaned_data['email'],],
            )
        except Exception as e:
            pass
            # TODO LOG this

        # try:
        for admin in settings.ADMINS:
            send_mail(
                'Поступило обращение к эксперту на сайте estz.su',
                '{} оставил обращение на рассмотрение эксперту на сайте estz.su. http://estz.su{}'.
                format(self.instance.full_name, reverse('admin-contact-expert-detail', args=[self.instance.id,])),
                settings.EMAIL_FROM,
                [admin[1]],
            )
        # except:
        #     pass

    # def __init__(self, *args, **kwargs):
    #     super(ContactAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ContactExpert
        fields = ['surname', 'name', 'patronymic', 'phone', 'email', 'post', 'work_place', 'file', 'message']

        widgets = {
            'message': Textarea(attrs={'rows': 15, }),
            'work_place': Textarea(attrs={'rows': 2, }),
        }


class ExpertResponseForm(ModelForm):
    # captcha = ReCaptchaField(widget=ReCaptchaWidget())
    # captcha = CaptchaField()

    # send emails to admin and user
    def send_emails(self):
        import datetime
        # try to send mail
        # msg_plain = render_to_string('contact/contact_admin_accepted.txt', {'username': self.cleaned_data['name']})
        for admin in settings.ADMINS:
            send_mail(
                'Поступил ответ от эксперта на сайте estz.su',
                '{} ответил на обращение: http://estz.su{} .'.
                format(self.instance.expert.name,
                       reverse('admin-contact-expert-detail', kwargs={'pk': self.instance.contact_expert_question.id})),
                settings.EMAIL_FROM,
                [admin[1]],
            )

    class Meta:
        model = ExpertResponse
        fields = ['subject', 'text', 'file']

        # widgets = {
        #     'message': Textarea(attrs={'rows': 15, }),
        #     'work_place': Textarea(attrs={'rows': 2, }),
        # }


