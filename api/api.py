# -*- coding: utf-8 -*-
import hashlib
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .serializes import *
import api.tasks as tasks
class ApiRoot(APIView):
    
    def get(self,request,format=None):
        return Response({
            'api': reverse('api-list'),
            'news-subcriber': reverse('news-subcriber'),
        })

class NewsSubcriber(generics.CreateAPIView):
    serializer_class = UserSubcriberNewsSerializer

    def get(self,request,format=None):
        serializer = self.get_serializer(data=request.GET)
        
        if 1: # just to resolveIndentation issue dur to editor
            try:
               serializer.is_valid(raise_exception=True)
            except Exception as e:
                messages.error(request, 'user subcriber news с таким электронной почтой уже существует.')
                return HttpResponseRedirect(settings.SITE_URL)
				
        code = serializer.validated_data['name']+\
            serializer.validated_data['email']+'estz'
        code = str(hashlib.sha1(code.encode('utf-8')).hexdigest().upper()[-20:])

        if code == request.GET.get('code'):
            try:
                serializer.create(serializer.validated_data)
                user = serializer.instance
                messages.success(request, 'Спасибо, вы успешно подписаны на новости.')
                return HttpResponseRedirect(settings.SITE_URL)
            except Exception as e:
                return HttpResponse(status=404)
        return HttpResponse(status=404)

    def post(self,request,format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['name']+\
            serializer.validated_data['email']+'estz'
        code = str(hashlib.sha1(code.encode('utf-8')).hexdigest().upper()[-20:])

        subject = 'Подписка на рассылку'
        html_content = render_to_string('emails/subcriber_news.html', {'name':serializer.validated_data['name'],
            'email':serializer.validated_data['email'],
            'code':code,})
        tasks.send_email(subject, html_content, [serializer.validated_data['email']])

        return Response({'status':1})


    def delete(self,request,format=None):
        if UserSubcriberNews.objects.filter(email=request.data.get('email')):
            user = UserSubcriberNews.objects.get(email=request.data.get('email'))
            user.delete()
            return Response({'status':1})
        raise Exception(_("This email is not found"))