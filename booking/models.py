from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='property_photos', blank=True)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    capacity = models.PositiveSmallIntegerField(default=2)
    is_available = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.property.name} - {self.name}"


    class Meta:
        ordering = ['name']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

class Book(models.Model):
    class Status(models.TextChoices):
        HOLD = "HOLD"
        RESERVED = "RESERVED"
        BOOKED = "BOOKED"
        CANCELLED = "CANCELLED"
        
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='booked_rooms')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.HOLD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        indexes = [
            models.Index(fields=['check_in_date', 'check_out_date']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['room_id', 'check_in_date', 'check_out_date']),
            models.Index(fields=['code']),
        ]
        ordering = ['-created_at']
        unique_together = ['room', 'check_in_date', 'check_out_date']
        constraints = [
            # exclusion constraint for booking same room on same date
            models.CheckConstraint(
                condition=models.Q(check_in_date__lt=models.F('check_out_date')),
                name='check_date_order'
            ),
        ]
        
class RatePlan(models.Model):
    code = models.CharField(max_length=80, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rate_plans')
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    min_nights = models.PositiveSmallIntegerField(default=1)
    max_nights = models.PositiveSmallIntegerField(null=True, blank=True)
    refundable = models.BooleanField(default=True)
    cancellation_deadline_days = models.PositiveSmallIntegerField(default=7)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.room.property.name} - {self.room.name} - {self.code}"
    
    class Meta:
        verbose_name = 'Rate Plan'
        verbose_name_plural = 'Rate Plans'
        ordering = ['room__property__name', 'room__name', 'code']
        unique_together = ['room', 'code']
        
