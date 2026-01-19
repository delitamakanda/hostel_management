from datetime import timedelta

from rest_framework.views import APIView
from django.utils.timezone import timezone, now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser

from booking.models import Book, Room, Property, RatePlan
from booking.serializers import BookCreateSerializer, BookSerializer, PropertySerializer, RoomSerializer, \
    RatePlanSerializer, RatePlanCreateSerializer
from booking.utils.pricing import calculate_occupancy_rate, calculate_revenue, calculate_no_shows


class BookCreateApiView(APIView):
    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            book = serializer.save()
            book.code = f"{book.id:06}"
            book.save()
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class BookDetailApiView(APIView):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class BookDetailConfirmApiView(APIView):
    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.status == 'HOLD':
                book.status = 'BOOKED'
                book.save()
                return Response({'message': 'Book confirmed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Book is already confirmed or cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        

class BookDetailCancelApiView(APIView):
    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.status == 'BOOKED' or book.status == 'HOLD'  and book.check_out_date > timezone.now()  and (book.check_out_date - timezone.now()).days >= 3:
                book.status = 'CANCELLED'
                book.save()
                return Response({'message': 'Book cancelled'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Book is already confirmed or cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class RoomListApiView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        property_id = request.query_params.get('property_id', None)
        qs = Room.objects.filter(is_available=True)
        if property_id:
            qs = qs.filter(property_id=property_id)
        return Response(RoomSerializer(qs.order_by("id"), many=True).data, status=status.HTTP_200_OK)
    

class PropertyListApiView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        qs = Property.objects.filter(is_active=True).order_by("name")
        return Response(PropertySerializer(qs, many=True).data, status=status.HTTP_200_OK)
    
    
class PropertyDetailRoomsApiView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, property_id):
        try:
            property = Property.objects.get(id=property_id)
            rooms = Room.objects.filter(property=property)
            check_in_date = request.query_params.get('check_in_date', None)
            check_out_date = request.query_params.get('check_out_date', None)
            guests = request.query_params.get('guests', None)
            if check_in_date and check_out_date:
                rooms = rooms.filter(check_in_date__gte=check_in_date, check_out_date__lte=check_out_date)
            if guests:
                rooms = rooms.filter(capacity__gte=int(guests))
            return Response(RoomSerializer(rooms, many=True).data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
    
    

class HealthCheckApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)
    
    
class AdminBookListAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        try:
            from_date = request.query_params.get('from', None)
            to_date = request.query_params.get('to', None)
            book_status = request.query_params.get('status', None)
            books = Book.objects.all()
            if from_date:
                books = books.filter(check_in_date__gte=from_date)
            if to_date:
                books = books.filter(check_out_date__lte=to_date)
            if status:
                books = books.filter(status=book_status)
            return Response(BookSerializer(books.order_by('-created_at'), many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AdminRoomDetailApiView(APIView):
    permission_classes = [IsAdminUser]
    
    def patch(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            room = serializer.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AdminRatePlanCreateApiView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        try:
            serializer = RatePlanCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            rate_plan = serializer.save()
            return Response(RatePlanSerializer(rate_plan).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AdminMetricsListApiView(APIView):
    permission_classes = [AllowAny,]
    
    def get(self, request):
        # occupancy, revenue, no-shows, etc.
        try:
            from datetime import datetime
            from_date_str = request.query_params.get('from', None)
            to_date_str = request.query_params.get('to', None)
            if from_date_str:
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
            else:
                from_date = now() - timedelta(days=30)
            
            if to_date_str:
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
            else:
                to_date = now() - timedelta(days=1)
            metrics = {'occupancy': float(0), 'revenue': float(0), 'no_shows': 0,
                       'from_date': from_date.strftime('%Y-%m-%d'), 'to_date': to_date.strftime('%Y-%m-%d')}
            occupancy_rate = calculate_occupancy_rate(from_date, to_date)
            metrics['occupancy'] = occupancy_rate
            revenue = calculate_revenue(from_date, to_date)
            metrics['revenue'] = revenue
            no_shows = calculate_no_shows(from_date, to_date)
            metrics['no_shows'] = no_shows
            return Response(metrics, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

