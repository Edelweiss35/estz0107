"""estz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from . import settings

import django.views.static
from .site_utils import error404

urlpatterns = [
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^', include('contact.urls')),
    url(r'^zadat-vopros-ekspertu/', include('contact.urls')),
    url(r'^admin-area/', include('admin_area.urls')),
    url(r'^', include('cms.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL.replace(settings.SITE_URL, ''), document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL.replace(settings.SITE_URL, ''), document_root=settings.MEDIA_ROOT)

urlpatterns += [
   url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
]

handler404 = error404