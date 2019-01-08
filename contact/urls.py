from django.conf.urls import url
from django.views.generic import TemplateView

from .views import ContactAdminView, ContactExpertView, ExpertResponseView

urlpatterns = [
    url(r'^napravit-obrashenie-administratoru-sajta/$', ContactAdminView.as_view(), name='contact-admin'),
    url(r'^zadat-vopros-ekspertu/$', ContactExpertView.as_view(), name='contact-admin'),
    url(r'^response-expert-to-client/(?P<slug>[0-9A-Za-z\-]+)/$', ExpertResponseView.as_view(), name='response-expert-to-client'),
    # url(r'^success$', TemplateView.as_view(template_name="contact/contact_admin_success.html"), name='contact-admin-success'),
]
