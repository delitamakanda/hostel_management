from django.urls import path
from booking import views
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.signup, name='signup'),
    path('hostels/<str:name>/', views.hostel_detail_view, name='hostel'),
    path('login/edit/', views.edit, name='edit'),
    path('login/select/', views.select, name='select'),
    path('register/login/edit/', views.edit, name='update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
