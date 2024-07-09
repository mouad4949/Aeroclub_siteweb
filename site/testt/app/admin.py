from django.contrib import admin
from .models import avions,News,Profile,Membership
# Register your models here.
admin.site.register(avions)
admin.site.register(News)
admin.site.register(Profile)
admin.site.register(Membership)