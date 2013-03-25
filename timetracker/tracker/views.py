from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.db.models import Sum

# Used to calculate dates, in timezones other than UTC
from datetime import datetime, timedelta
from pytz import timezone
import pytz

# Used for exporting CSV information
import csv
import unicodecsv
from cStringIO import StringIO

from tracker.forms import *
from django.contrib.auth.models import User


# Sets up a new WorkDuration when a new WorkEntry is created and it isRunning is true
def newDuration(request, form):
	if form.cleaned_data['isRunning']:
		entry = WorkEntry.objects.get(customer=form.cleaned_data['customer'], project=form.cleaned_data['project'], task=form.cleaned_data['task'])
		entry.isRunning = True
		entry.lastWorkedDate = timezone('US/Eastern').localize(datetime.now()).date()
		entry.save()
		duration = WorkDuration(workEntry=entry, user=request.user, start=timezone('US/Eastern').localize(datetime.now()), isCurrent=True)
		duration.save()

# Display every work entry
@login_required
def all_entries(request):
	workEntries = WorkEntry.objects.filter(user=request.user)
	user = request.user
	time = workEntries.aggregate(total=Sum('totalTime'))
	allEntries = True
	today = timezone('US/Eastern').localize(datetime.now()).date()

	newEntry = WorkEntry(user=request.user, lastWorkedDate=timezone('US/Eastern').localize(datetime.now()).date())
	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=newEntry)
		if form.is_valid():
			form.save()
			newDuration(request, form)
			return HttpResponseRedirect('/all')
	else:
		form = WorkEntryForm(instance=newEntry)
	return render(request, 'index.html', locals())

# Display work entries either created or worked on today
@login_required
def today(request):
	user = request.user
	today = timezone('US/Eastern').localize(datetime.now()).date()
	workEntries = WorkEntry.objects.filter(user=user, lastWorkedDate__day=today.day, lastWorkedDate__month=today.month, lastWorkedDate__year=today.year)
	yesterday = today - timedelta(1)
	newEntry = WorkEntry(user=user, lastWorkedDate=timezone('US/Eastern').localize(datetime.now()).date())
	time = workEntries.aggregate(total=Sum('totalTime'))

	if request.method == 'POST':
		form = WorkEntryForm(request.POST,instance=newEntry)
		if form.is_valid():
			form.save()
			newDuration(request, form)
			return HttpResponseRedirect('/today')
	else:
		form = WorkEntryForm(instance=newEntry)
	return render(request, 'index.html', locals())

# Display work entries last worked on a given date
@login_required
def date(request, year, month, day):
	user = request.user
	workEntries = WorkEntry.objects.filter(user=user, lastWorkedDate__day=day, lastWorkedDate__month=month, lastWorkedDate__year=year)
	time = workEntries.aggregate(total=Sum('totalTime'))
	theDate = timezone('US/Eastern').localize(datetime(int(year), int(month), int(day))).date()

	if theDate == timezone('US/Eastern').localize(datetime.now()).date():
		response = today(request)
	else:
		yesterday = theDate - timedelta(1)
		tomorrow = theDate + timedelta(1)

		newEntry = WorkEntry(user=user, lastWorkedDate=timezone('US/Eastern').localize(datetime.now()).date())
		if request.method == 'POST':
			form = WorkEntryForm(request.POST,instance=newEntry)
			if form.is_valid():
				form.save()
				newDuration(request, form)
				return HttpResponseRedirect('/today')
		else:
			form = WorkEntryForm(instance=newEntry)

		response = render(request, 'index.html', locals())
	return response

# Used to update already made WorkEntry
@login_required
def update_form(request, entryId):
	entry = WorkEntry.objects.get(id=int(entryId))
	if request.method == 'POST':
		form = WorkEntryForm(request.POST, instance=entry)
		if form.is_valid:
			form.save()
			return HttpResponseRedirect('/today')
	else:
		form = WorkEntryForm(instance=entry)
	return render(request, 'add_form.html', locals())

# Used to add new WorkEntry, Customer, and Project
@login_required
def add_form(request, formType):
	if formType == 'work':
		newEntry = WorkEntry(user=request.user, lastWorkedDate=timezone('US/Eastern').localize(datetime.now()).date())
		if request.method == 'POST':
			form = WorkEntryForm(request.POST,instance=newEntry)
			if form.is_valid():
				form.save()
				newDuration(request, form)
				return HttpResponseRedirect('/today')
		else:
			form = WorkEntryForm(instance=newEntry)
	elif formType == 'customer':
		newEntry = Customer()
		if request.method == 'POST':
			form = CustomerForm(request.POST,instance=newEntry)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/today')
		else:
			form = CustomerForm(instance=newEntry)
	elif formType == 'project':
		newEntry = Project()
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance=newEntry)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/today')
		else:
			form = ProjectForm(instance=newEntry)
	else:
		raise Http404
	return render(request, 'add_form.html', locals())

# Starts a WorkDuration timer
@login_required
def start_task(request, entry):
	entry = WorkEntry.objects.get(id=entry)
	if(entry.isRunning):
		return HttpResponseRedirect('/today') # add error message, entry already running
	else:
		entry.isRunning = True
		entry.lastWorkedDate = timezone('US/Eastern').localize(datetime.now()).date()
		entry.save()
		duration = WorkDuration(workEntry=entry, user=request.user, start=timezone('US/Eastern').localize(datetime.now()), isCurrent=True)
		duration.save()
	return HttpResponseRedirect('/today')

# Stops a WorkDuration timer
@login_required
def stop_task(request, entry):
	entry = WorkEntry.objects.get(id=entry) 
	duration = entry.workduration_set.get(isCurrent=True) # get current duration
	duration.end = timezone('US/Eastern').localize(datetime.now())
	duration.isCurrent = False
	duration.save()
	entry.isRunning = False
	timedelta = duration.end - duration.start
	entry.totalTime += round((timedelta.total_seconds()/3600),2)
	entry.save()
	return HttpResponseRedirect('/today')

# Creates list of customers for which the requesting user has done 
@login_required
def billing(request):
	customersList = WorkEntry.objects.filter(user=request.user).values_list("customer").distinct()
	customers = Customer.objects.filter(id__in=customersList)
	return render(request, 'billing.html', locals())

# Displays billing info from a user for a given customer
@login_required
def customer_billing(request, customer):
	theCustomer = Customer.objects.get(company=customer)
	workEntries = WorkEntry.objects.filter(user=request.user, customer=theCustomer)
	return render(request, 'customer_billing.html', locals())

# Displays list of WorkEntries that can be exported to CSV
@login_required
def choose_csv(request):
	workEntries = WorkEntry.objects.filter(user=request.user)
	return render(request, 'choose_csv.html', locals())

# Exports a given WorkEntry to CSV
@login_required
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
