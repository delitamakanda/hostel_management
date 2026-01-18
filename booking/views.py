from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from booking.models import Book, Room, Property
from booking.serializers import BookCreateSerializer, BookSerializer, PropertySerializer, RoomSerializer


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
    

class HealthCheckApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)
