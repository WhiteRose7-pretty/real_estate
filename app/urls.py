from django.urls import path
from . import views


app_name = 'app'



urlpatterns = [
    path('', views.home, name='home'),
    path('property-likes/', views.property_likes, name='video_likes'),
    path('update/', views.update, name='update')
]