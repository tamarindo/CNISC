from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(App)
admin.site.register(CuentaSocial)
admin.site.register(TokenSocial)



