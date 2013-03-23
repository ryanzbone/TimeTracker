from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from tracker.models import WorkEntry
from django.contrib.auth.models import User

@login_required
def index(request):
	workEntries = WorkEntry.objects.filter(user=User)
	user = User
	return render(request, 'index.html', locals())
