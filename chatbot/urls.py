from django.urls import path 
from . import views #to import the views module in this file
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', views.index, name="index"),  
    path('register/',views.register,name="register"),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
    path('process_message/', views.process_message, name='process_message'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)