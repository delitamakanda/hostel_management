from django.urls import path
from booking import views

urlpatterns = [
    path('book/', views.BookCreateApiView.as_view(), name='book-create'),
    path('book/<int:book_id>/', views.BookDetailApiView.as_view(), name='book-detail'),
    path('rooms/', views.RoomListApiView.as_view(), name='room-list'),
    path('book/<int:book_id>/confirm/', views.BookDetailConfirmApiView.as_view(), name='book-detail-confirm'),
    path('book/<int:book_id>/cancel/', views.BookDetailCancelApiView.as_view(), name='book-detail-cancel'),
    path('properties/', views.PropertyListApiView.as_view(), name='property-list'),
    path('property/<int:property_id>/rooms/', views.PropertyDetailRoomsApiView.as_view(), name='property-room-list'),
    path('healthcheck/', views.HealthCheckApiView.as_view(), name='healthcheck'),
    path('admin/books/', views.AdminBookListAPIView.as_view(), name='book-admin-list'),
    path('admin/books/<int:book_id>/', views.AdminRoomDetailApiView.as_view(), name='book-admin-detail'),
    path('admin/rate-plans/', views.AdminRatePlanCreateApiView.as_view(), name='rate-plan-admin-list'),
    path('admin/metrics/', views.AdminMetricsListApiView.as_view(), name='metrics-admin-list'),
]
