from django.conf.urls import *
from . import views
urlpatterns = [
            # url(r'^view_profile/$', 'views.view_profile', name ='view_profile'),
            url(r'^view_profile/edit_profile/$', views.edit_profile, name ='edit_profile')
]
