from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	company = models.CharField(max_length = 50)
	address1 = models.CharField(max_length = 50, blank=True)
	address2 = models.CharField(max_length = 50, blank=True)
	address3 = models.CharField(max_length = 50, blank=True)
	city = models.CharField(max_length = 50, blank=True)
	state = models.CharField(max_length = 2, blank=True)
	zipCode = models.CharField(max_length = 15, blank=True)
	phone1 = models.CharField(max_length = 20, blank=True)
	phone2 = models.CharField(max_length = 20, blank=True)
	fax1 = models.CharField(max_length = 20, blank=True)
	fax2 = models.CharField(max_length = 20, blank=True)
	email1 = models.EmailField(blank=True)
	email2 = models.EmailField(blank=True)
	email3 = models.EmailField(blank=True)
	website = models.URLField(blank=True)

	def __unicode__(self):
		return self.company

class Project(models.Model):
	title = models.CharField(max_length=50)
	customer = models.ForeignKey('Customer')
	totalTime = models.FloatField(blank=True)

	def __unicode__(self):
		return self.title

class WorkEntry(models.Model):
	user = models.ForeignKey(User)
	customer = models.ForeignKey('Customer')
	project = models.OneToOneField('Project')
	beginDateTime = models.DateTimeField()
	endDateTime = models.DateTimeField(blank=True, null=True)
	totalTime = models.FloatField(blank=True)
	task = models.TextField(blank=True)
