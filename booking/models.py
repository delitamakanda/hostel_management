from django.db import models
from django.contrib.auth.models import User

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    enrollment_no = models.CharField(max_length=20)
    date_of_birth = models.DateField(max_length=10, help_text='format: DD/MM/YYYY')
    gender = models.CharField(max_length=10, choices=gender_choices)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    room_alloted = models.BooleanField(default=False)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, default=None, blank=True)

    def __str__(self):
        return self.guest_name

    class Meta:
        ordering = ['-date_of_birth']
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

class Room(models.Model):
    room_choices = [('S', 'Single'), ('D', 'Double'), ('P', 'Reserved'), ('B', 'Both')]
    room_no = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=1, choices=room_choices)
    vacant = models.BooleanField(default=False)
    hostel = models.ForeignKey('Hostel', on_delete=models.CASCADE)

    def __str__(self):
        return self.room_no

    class Meta:
        ordering = ['-room_no']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

class Hostel(models.Model):
    name = models.CharField(max_length=100)
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    warden = models.CharField(max_length=100)
    caretaker = models.CharField(max_length=100)
    book = models.ManyToManyField('Book', default=None, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'

class Book(models.Model):
    code = models.CharField(max_length=20)
    room_choice = [('S', 'Single'), ('D', 'Double'), ('P', 'Reserved'), ('B', 'Both')]
    room_type = models.CharField(max_length=1, choices=room_choice, default='S')

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-code']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
