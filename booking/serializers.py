import time
from rest_framework import serializers
from django.contrib.auth.models import User
from booking.models import Book, Room, Guest, Hostel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'guest_name', 'guest_email', 'enrollment_no', 'date_of_birth', 'gender', 'room', 'room_alloted', 'book')
        read_only_fields = ('id',)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'code', 'room_type')
        read_only_fields = ('id',)

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_no', 'name', 'room_type', 'vacant', 'hostel')
        read_only_fields = ('id',)

classic_hostels = ['Freedom',]

class HostelSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Hostel
        fields = ('id', 'name', 'gender', 'warden', 'caretaker', 'book')
        read_only_fields = ('id',)

    def to_representation(self, obj):
        data = super(HostelSerializer, self).to_representation(obj)
        if data['name'] in classic_hostels:
            data['is_classic_hostel'] = True
        else:
            data['is_classic_hostel'] = False
            time.sleep(1)
        return data

