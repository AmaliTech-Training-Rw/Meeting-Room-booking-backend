from django.contrib import admin
from .models import Employee,MeetingRoom,Booking
# Register your models here.

admin.site.register(Employee)
admin.site.register(MeetingRoom)
admin.site.register(Booking)