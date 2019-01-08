from datetime import timedelta, datetime
from celery.decorators import task
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import UserSubcriberNews
from aldryn_newsblog.models import ArticleTranslation
def send_email(subject, html_content, emails, from_email=None):
    if from_email is None:
        from_email = settings.EMAIL_FROM

    msg = mail.EmailMessage(subject, html_content, from_email, emails)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.mixed_subtype = 'related'

    return msg.send()
	
@task()	
def send_newsletters():
	yesterday = (datetime.today()-timedelta(days=1))
	yesterday = yesterday.replace(hour=8, minute=30)
	
	articles = ArticleTranslation.objects.filter(master__publishing_date__gt=yesterday, master__is_published=True)
	
	subscribers = UserSubcriberNews.objects.all()
	for subscriber in subscribers:
		html_content = render_to_string('emails/newsletter.html', {'subscriber':subscriber,
				'articles':articles})
		
		msg = mail.EmailMessage('Newsletter', html_content, settings.EMAIL_FROM, [subscriber.email])
		msg.content_subtype = "html"  # Main content is now text/html
		msg.mixed_subtype = 'related'

		msg.send()
	