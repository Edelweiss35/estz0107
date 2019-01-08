from django.conf.urls import url
from django.views.generic import TemplateView

from .views import AdminIndexView, AdminContactListView, AdminContactDetailView, change_status, \
    change_contactexpert_status, AdminContactExpertListView, AdminContactExpertDetailView, send_to_experts

urlpatterns = [
    url(r'^$', AdminIndexView.as_view(), name='admin-index'),
    url(r'^contact/$', AdminContactListView.as_view(), name='admin-contact-list'),
    url(r'^contact/(?P<pk>[0-9]+)/$', AdminContactDetailView.as_view(), name='admin-contact-detail'),
    url(r'^contact/response-success/$',
        TemplateView.as_view(template_name="admin_area/response_success.html"),
        name='admin-contact-response-success'),
    url(r'^contact/change-status/$', change_status, name='admin-contact-change_status'),
    url(r'^contact-expert/$', AdminContactExpertListView.as_view(), name='admin-contact-expert-list'),
    url(r'^contact-expert/(?P<pk>[0-9]+)/send-experts/$', send_to_experts, name='admin-contact-expert-send-expert'),
    url(r'^contact-expert/(?P<pk>[0-9]+)/$', AdminContactExpertDetailView.as_view(), name='admin-contact-expert-detail'),
    # url(r'^contact-expert/response-success/$', TemplateView.as_view(template_name="admin_area/response_success.html"),
    #     name='admin-contact-response-success'),
    url(r'^contact-expert/change-status/$', change_contactexpert_status, name='expert-contact-change_status'),
]
