from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class Employee(models.Model):
    # user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    email = models.EmailField(max_length = 254)
    # password=
    location = models.CharField(max_length=50)
    # role=
    
    
    # returns the object representation in a string format
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class MeetingRoom(models.Model):
    room_name = models.CharField(max_length=50)
    number_of_people = models.IntegerField(default=0)
    description = models.CharField(max_length=250)
    equipments = models.ManyToManyField('equipments.Equipment')
    services = models.ManyToManyField('services.Service')
    
    def __str__(self):
        return self.room_name

class Booking(models.Model):
    STATUS=(('Available','Available'),
            ('Not available','Not available'))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    status= models.CharField(max_length=250, null =True, choices= STATUS)
    date= models.DateField()
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time')
    