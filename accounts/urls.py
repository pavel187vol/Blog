from django.conf.urls import url
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

# SET THE NAMESPACE!
add_name = 'Skittel'
app_name = 'account'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.SignUp.as_view(),name='register'),
    url(r'^view_profile/$', views.view_profile, name ='view_profile'),
    path('details/<username>/', views.details_profile, name ='details_profile'),
    url(r'^view_profile/edit_profile/<int:pk>/$', views.edit_profile, name ='edit_profile'),
    path('change/password/',auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'), name='change-password'),
    path('change/password/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/done-chane-password.html'), name='change-password-done'),
    path('password/reset/form/',auth_views.PasswordResetView.as_view(template_name='registration/form_reset_password.html'), name='change-password-form'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/confirm_reset_password.html'), name='password_reset_confirm'),
    path('password/reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/complete_reset_password.html'), name='change-password-complete'),
    path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/done_reset_password.html'), name='change-password-done'),

    # url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    # url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),


]
