from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
import datetime
from datetime import date, timedelta
import csv
import unicodecsv
from cStringIO import StringIO

from tracker.models import WorkEntry
from tracker.forms import *
from django.contrib.auth.models import User

@login_required
def all_entries(request):
	workEntries = WorkEntry.objects.filter(user=request.user)
	user = request.user
	time = workEntries.aggregate(total=Sum('totalTime'))
	allEntries = True
	today = now().date()

	exp = WorkEntry(user=request.user)
	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=exp)
		if form.is_valid():
			form.save()
			newDuration(request, form)
			return HttpResponseRedirect('/all')
	else:
		form = WorkEntryForm(instance=exp)

	return render(request, 'index.html', locals())

@login_required
def today(request):
	today = now().date()
	workEntries = WorkEntry.objects.filter(user=request.user, lastWorkedDate__day=today.day, lastWorkedDate__month=today.month, lastWorkedDate__year=today.year)
	yesterday = today - timedelta(1)
	user = request.user
	exp = WorkEntry(user=request.user)
	time = workEntries.aggregate(total=Sum('totalTime'))

	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=exp)
		if form.is_valid():
			form.save()
			newDuration(request, form)
			return HttpResponseRedirect('/today')
	else:
		form = WorkEntryForm(instance=exp)

	return render(request, 'index.html', locals())

@login_required
def date(request, year, month, day):
	workEntries = WorkEntry.objects.filter(user=request.user, lastWorkedDate__day=day, lastWorkedDate__month=month, lastWorkedDate__year=year)
	user = request.user
	exp = WorkEntry(user=request.user)
	time = workEntries.aggregate(total=Sum('totalTime'))
	theDate = datetime.date(int(year), int(month), int(day))
	yesterday = theDate - timedelta(1)
	tomorrow = theDate + timedelta(1)

	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=exp)
		if form.is_valid():
			form.save()
			newDuration(request, form)
			return HttpResponseRedirect('/today')
	else:
		form = WorkEntryForm(instance=exp)

	return render(request, 'index.html', locals())

def newDuration(request, form):
	if form.cleaned_data['isRunning']:
		entry = WorkEntry.objects.get(customer=form.cleaned_data['customer'], project=form.cleaned_data['project'], task=form.cleaned_data['task'])
		entry.isRunning = True
		entry.lastWorkedDate = now()
		entry.save()
		duration = WorkDuration(workEntry=entry, user=request.user, start=now(), isCurrent=True)
		duration.save()




@login_required
def update_form(request, entryId):
	entry = WorkEntry.objects.get(id=int(entryId))
	if request.method == 'POST':
		form = WorkEntryForm(request.POST, instance=entry)
		if form.is_valid:
			form.save()
			# newDuration(request, updateForm)
			return HttpResponseRedirect('/today')
	else:
		form = WorkEntryForm(instance=entry)
	return render(request, 'add_form.html', locals())




@login_required
def add_form(request, formType):
	if formType == 'work':
		exp = WorkEntry(user=request.user)
		if request.method == 'POST':
			form = WorkEntryForm(request.POST,instance=exp)
			if form.is_valid():
				form.save()
				newDuration(request, form)
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

@login_required
def billing(request):
	user = request.user
	workEntries = WorkEntry.objects.filter(user=user)

	return render(request, 'billing.html', locals())

@login_required
def customer_billing(request, customer):
	user = request.user
	theCustomer = Customer.objects.get(company=customer)
	workEntries = WorkEntry.objects.filter(user=user, customer=theCustomer)

	return render(request, 'customer_billing.html', locals())

def choose_csv(request):
	workEntries = WorkEntry.objects.filter(user=request.user)
	return render(request, 'choose_csv.html', locals())

def export_csv(request, entryId):
    # Create the HttpResponse object with the appropriate CSV header.
	theEntry = WorkEntry.objects.get(id=entryId)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="WorkEntries.csv"'
	# f = StringIO()
	w = unicodecsv.writer(response, encoding='utf-8')
	w.writerow((u'Customer', u'Project', u'Task', u'Notes', u'Total Time (hours)'))
	w.writerow((theEntry.customer, theEntry.project, theEntry.task, theEntry.notes, theEntry.totalTime))
	w.writerow((u'Start Date Time', u'End Date Time'))
	for duration in theEntry.workduration_set.all():
		w.writerow((duration.start, duration.end))
	return response
