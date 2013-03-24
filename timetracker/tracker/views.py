from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.utils.timezone import now

from tracker.models import WorkEntry
from tracker.forms import *
from django.contrib.auth.models import User

@login_required
def all_entries(request):
	workEntries = WorkEntry.objects.filter(user=request.user)
	user = request.user

	exp = WorkEntry(user=request.user)
	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=exp)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/today')
	else:
		form = WorkEntryForm(instance=exp)

	return render(request, 'index.html', locals())

@login_required
def today(request):
	today = now().date()
	workEntries = WorkEntry.objects.filter(user=request.user, 
		lastWorkedDate__day=today.day, lastWorkedDate__month=today.month, lastWorkedDate__year=today.year)

	user = request.user
	exp = WorkEntry(user=request.user)
	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=exp)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/today')
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
				return HttpResponseRedirect('/today')
		else:
			form = WorkEntryForm(instance=exp)
	elif formType == 'customer':
		exp = Customer()
		if request.method == 'POST':
			form = CustomerForm(request.POST,instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/today')
		else:
			form = CustomerForm(instance=exp)
	elif formType == 'project':
		exp = Project()
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance=exp)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/today')
		else:
			form = ProjectForm(instance=exp)
	else:
		raise Http404
	return render(request, 'add_form.html', locals())

@login_required
def start_task(request, entry):
	entry = WorkEntry.objects.get(id=entry)
	if(entry.isRunning):
		return HttpResponseRedirect('/today') # add error message, entry already running
	else:
		entry.isRunning = True
		entry.lastWorkedDate = now()
		entry.save()
		duration = WorkDuration(workEntry=entry, user=request.user, start=now(), isCurrent=True)
		duration.save()

	return HttpResponseRedirect('/today')

@login_required
def stop_task(request, entry):
	entry = WorkEntry.objects.get(id=entry) 
	duration = entry.workduration_set.get(isCurrent=True) # get current duration
	duration.end = now()
	duration.isCurrent = False
	duration.save()
	entry.isRunning = False
	timedelta = duration.end - duration.start
	entry.totalTime += round((timedelta.total_seconds()/3600),2)
	entry.save()

	return HttpResponseRedirect('/today')



# @login_required
# def billing(request):



# @login_required
# def customer_billing(request, customer):



