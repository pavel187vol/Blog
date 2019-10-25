from django.conf.urls import url
from django.urls import path
from . import views
# SET THE NAMESPACE!
add_name = 'Skittel'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^view_profile/$', views.view_profile, name ='view_profile'),
    path('details/<int:pk>/', views.details_profile, name ='details_profile'),
    url(r'^view_profile/edit_profile/<int:pk>/$', views.edit_profile, name ='edit_profile'),

]
