from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(UserExt)
admin.site.register(ConfUser)
admin.site.register(Profile)
admin.site.register(Graduate)
admin.site.register(Student)
admin.site.register(Message)
admin.site.register(View_Messages_User)
admin.site.register(Attachment)
