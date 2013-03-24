from django.contrib import admin
from models import *

class WorkDurationInline(admin.StackedInline):
	model = WorkDuration 
	extra = 0

class WorkEntryInline(admin.StackedInline):
	model = WorkEntry
	extra = 0

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'first_name', 'last_name', 'email',)
	search_fields = ('username', 'first_name', 'last_name', 'email',)
	inlines = [
    	WorkEntryInline, WorkDurationInline
    ]

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('company', 'phone1', 'email1', 'website',)
	search_fields = ('company', 'website',)
	list_filter = ('state',)

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'customer', 'totalTime',)
	search_fields = ('title', 'customer',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Project, ProjectAdmin)