# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

# from . import DEFAULT_APP_NAMESPACE


class CalcApp(CMSApp):
    name = _('Calc')
    app_name = 'asdf'
    # urls = ['aldryn_people.urls']  # COMPAT: CMS3.2

    def get_urls(self, *args, **kwargs):
        return []


apphook_pool.register(CalcApp)
