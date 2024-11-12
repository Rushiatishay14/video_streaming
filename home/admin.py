from django.contrib import admin

from .models import UserMaster,UserActivityTracking

# Register your models here.
admin.site.register(UserMaster)
admin.site.register(UserActivityTracking)