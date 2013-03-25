from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey 

class Customer(models.Model):
	company = models.CharField(max_length = 50)
	address1 = models.CharField('address 1', max_length = 50, blank=True)
	address2 = models.CharField('address 2', max_length = 50, blank=True)
	address3 = models.CharField('address 3', max_length = 50, blank=True)
	city = models.CharField(max_length = 50, blank=True)
	state = models.CharField(max_length = 2, blank=True)
	zipCode = models.CharField('zip code', max_length = 15, blank=True)
	phone1 = models.CharField('phone 1', max_length = 20, blank=True)
	phone2 = models.CharField('phone 2', max_length = 20, blank=True)
	fax1 = models.CharField('fax 1', max_length = 20, blank=True)
	fax2 = models.CharField('fax 2', max_length = 20, blank=True)
	email1 = models.EmailField('email 1', blank=True)
	email2 = models.EmailField('email 2', blank=True)
	email3 = models.EmailField('email 3', blank=True)
	website = models.URLField(blank=True)

	def __unicode__(self):
		return self.company

	class Meta:
		ordering = ['company']


class Project(models.Model):
	title = models.CharField(max_length=50)
	customer = models.ForeignKey('Customer')
	totalTime = models.FloatField('total time', default=0)

	def __unicode__(self):
		return self.title

class WorkEntry(models.Model):
	user = models.ForeignKey(User)
	customer = models.ForeignKey('Customer')
	# project = models.ForeignKey('Project')
	project = ChainedForeignKey(
		Project,
		chained_field="customer",
		chained_model_field="customer",
		show_all=False,
		auto_choose=True
	)
	totalTime = models.FloatField('total time', default=0)
	task = models.CharField(max_length=100)
	notes = models.TextField(blank=True)
	isRunning = models.BooleanField('is current project', default=False)
	lastWorkedDate = models.DateField('last worked date', blank = True, null=True)

	def __unicode__(self):
		return u'%s (%s)' %(self.task, self.project)

	class Meta:
		ordering = ['-isRunning']
		verbose_name = "work entry"
		verbose_name_plural = "work entries"


class WorkDuration(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField(blank=True, null=True)
	user = models.ForeignKey(User)
	workEntry = models.ForeignKey('WorkEntry')
	isCurrent = models.BooleanField('is current work duration', default=False)

	def duration(self):
		return timedelta

	class Meta:
		ordering = ['-start']
		verbose_name = "work duration"