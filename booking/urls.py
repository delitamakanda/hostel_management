from django.urls import path
from booking import views

urlpatterns = [
    path('book/', views.BookCreateApiView.as_view(), name='book-create'),
    path('book/<int:book_id>/', views.BookDetailApiView.as_view(), name='book-detail'),
    path('rooms/', views.RoomListApiView.as_view(), name='room-list'),
    path('properties/', views.PropertyListApiView.as_view(), name='property-list'),
    path('healthcheck/', views.HealthCheckApiView.as_view(), name='healthcheck'),
]
