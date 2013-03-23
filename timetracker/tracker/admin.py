from django.contrib import admin
from models import *

class WorkEntryInline(admin.StackedInline):
	model = WorkEntry
	extra = 0

admin.site.register(Customer)
admin.site.register(Project)
admin.site.register(WorkEntry)