from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('', views.dashboard, name='dashboard'),
    path('view_profile/', views.view_profile, name ='view_profile'),
    path('details/<username>/', views.details_profile, name ='details_profile'),
    path('<username>/', views.my_profile, name ='my_profile'),
    path('remove/<username>/', views.remove_profile, name ='remove_profile'),
]
