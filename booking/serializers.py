import time
from rest_framework import serializers
from booking.models import Book, Room, Property, RatePlan


class RatePlanCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RatePlan
        fields = ('id', 'code', 'price_per_night', 'min_nights', 'max_nights', 'refundable', 'cancellation_deadline_days', 'is_active', 'room_id')
        read_only_fields = ('id',)
    
    def validate(self, attrs):
        if attrs['max_nights'] is not None and attrs['max_nights'] < attrs['min_nights']:
            raise serializers.ValidationError("Max nights must be greater than or equal to min nights.")
        return attrs
    
    def create(self, validated_data):
        room_id = validated_data['room_id']
        room = Room.objects.get(id=room_id)
        rate_plan = RatePlan.objects.create(
            room=room,
            code=validated_data['code'],
            price_per_night=validated_data['price_per_night'],
            min_nights=validated_data['min_nights'],
            max_nights=validated_data['max_nights'],
            refundable=validated_data['refundable'],
            cancellation_deadline_days=validated_data['cancellation_deadline_days'],
            is_active=validated_data['is_active'],
        )
        return rate_plan


class RatePlanSerializer(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField()
    
    class Meta:
        model = RatePlan
        fields = ('code', 'price_total', 'refundable',)
        read_only_fields = ('price_total',)
    
    def get_price_total(self, obj):
        price_per_night = obj.price_per_night
        min_nights = obj.min_nights
        max_nights = obj.max_nights
        if max_nights is None:
            return price_per_night * min_nights
        return price_per_night * (max_nights - min_nights + 1)


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
    rates = RatePlanSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ('id', 'name', 'property', 'capacity', 'is_available', 'rates',)
        read_only_fields = ('id',)


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'name', 'location', 'is_active',)
        read_only_fields = ('id',)
