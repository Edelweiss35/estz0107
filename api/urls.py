from django.conf.urls import include, url
import api.api as api_views

urlpatterns = [
    url(r'^$', api_views.ApiRoot.as_view(), name='api-list'),
    url(r'^news/subcriber/$', api_views.NewsSubcriber.as_view(), name='news-subcriber'),
]