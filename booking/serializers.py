import time
from rest_framework import serializers
from booking.models import Book, Room, Property


class BookCreateSerializer(serializers.ModelSerializer):
    room_id =serializers.IntegerField()
    checkin_date = serializers.DateField()
    checkout_date = serializers.DateField()
    
    class Meta:
        model = Book
        fields = ('id', 'room_id', 'checkin_date', 'checkout_date', 'status', 'created_at', 'updated_at',)
        
    def validate(self, attrs):
        if attrs['checkin_date'] >= attrs['checkout_date']:
            raise serializers.ValidationError("Check-out date must be greater than check-in date.")
        return attrs
    
    def create(self, validated_data):
        room_id = validated_data['room_id']
        checkin_date = validated_data['checkin_date']
        checkout_date = validated_data['checkout_date']
        return Book.objects.create(
            room_id=room_id,
            check_in_date=checkin_date,
            check_out_date=checkout_date,
            status='pending',
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        )
    
    
class BookSerializer(serializers.ModelSerializer):
    checkin = serializers.SerializerMethodField()
    checkout = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ('id', 'room', 'checkin', 'checkout', 'status', 'created_at', 'updated_at',)
        read_only_fields = ('id',)
        
    def get_checkin(self, obj):
        return obj.check_in_date.strftime("%Y-%m-%d")
    
    def get_checkout(self, obj):
        return obj.check_out_date.strftime("%Y-%m-%d")

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'property', 'capacity', 'is_available',)
        read_only_fields = ('id',)


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'name', 'location', 'is_active',)
        read_only_fields = ('id',)


