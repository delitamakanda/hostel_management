from django.urls import path
from users import views

urlpatterns = [
    path('me/', views.MeViewAPIView.as_view(), name='me-view'),
    path('signup/', views.SignupAPIView.as_view(), name='signup-view'),
]