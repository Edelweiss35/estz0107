from __future__ import unicode_literals

from django.db import models

class UserSubcriberNews(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200,unique=True)

	def __unicode__(self):
		return self.email