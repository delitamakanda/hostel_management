from django.urls import path
from booking import views
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('healthcheck/', views.HealthCheckApiView.as_view(), name='healthcheck'),
]

urlpatterns += router.urls
