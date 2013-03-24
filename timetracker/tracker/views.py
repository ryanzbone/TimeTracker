from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from datetime import date


from tracker.models import WorkEntry
from tracker.forms import *
from django.contrib.auth.models import User

@login_required
def index(request):
	today = date.today()
	workEntries = WorkEntry.objects.filter(user=request.user)
	user = request.user

	exp = WorkEntry(user=request.user)
	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=exp)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = WorkEntryForm(instance=exp)

	return render(request, 'index.html', locals())

@login_required
def add_form(request, formType):
	if formType == 'work':
		exp = WorkEntry(user=request.user)
		if request.method == 'POST':
			form = WorkEntryForm(request.POST,instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')
		else:
			form = WorkEntryForm(instance=exp)
	elif formType == 'customer':
		exp = Customer()
		if request.method == 'POST':
			form = CustomerForm(request.POST,instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')
		else:
			form = CustomerForm(instance=exp)
	elif formType == 'project':
		exp = Project()
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/')
		else:
			form = ProjectForm(instance=exp)
	else:
		raise Http404
	return render(request, 'add_form.html', locals())

# @login_required
# def billing(request):
	


# @login_required
# def customer_billing(request, customer):
	


