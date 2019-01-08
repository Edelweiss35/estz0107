from django.shortcuts import render

from django.template import RequestContext

def error404(request):
	return render(request,'errors/404.html')
