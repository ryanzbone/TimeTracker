from django import forms
from tracker.models import *
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project 

class WorkEntryForm(forms.ModelForm):
	class Meta:
		model = WorkEntry
		exclude = ('user',)
		# widgets = {
		# 	'customer': 
		# }
