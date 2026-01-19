from django.db.models import Q, Sum

from booking.models import Book, Room


def calculate_occupancy_rate(from_date, to_date) -> float:
    from django.db.models import Count, Q
    bookings = Book.objects.filter(
        Q(check_in_date__range=(from_date, to_date)) | Q(check_out_date__range=(from_date, to_date))
    ).annotate(count=Count('id')).values('count')
    total_bookings = sum([booking['count'] for booking in bookings])
    total_rooms = Room.objects.count()
    if total_rooms == 0:
        return 0.0  # No rooms available to book during the given date range
    occupancy_rate = (total_bookings / total_rooms) * 100
    return occupancy_rate

def calculate_revenue(from_date, to_date) -> float:
    from booking.models import Book
    bookings = Book.objects.filter(
        Q(check_in_date__range=(from_date, to_date)) | Q(check_out_date__range=(from_date, to_date))
    ).annotate(revenue=Sum('room__rate_plans__price_per_night') * Sum('room__rate_plans__min_nights')).values('revenue')
    total_revenue = sum([booking['revenue'] for booking in bookings])
    return total_revenue

def calculate_no_shows(from_date, to_date) -> int:
    from booking.models import Book
    no_shows = Book.objects.filter(
        Q(check_out_date__lt=from_date) | Q(check_in_date__gt=to_date)
    ).count()
    return no_shows