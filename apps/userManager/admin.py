from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(UserExt)
admin.site.register(Profile)
admin.site.register(ProfileMeta)
admin.site.register(TempKeys)
