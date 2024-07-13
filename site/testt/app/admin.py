from django.contrib import admin
from .models import avions,News,Profile,Membership,Services,Reservation
# Register your models here.
admin.site.register(avions)
admin.site.register(News)
admin.site.register(Profile)
admin.site.register(Membership)
admin.site.register(Services)
admin.site.register(Reservation)