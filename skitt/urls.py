from django.urls import path
from . import views
from django.conf.urls import url



urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('post/<id>/<slug>/', views.post_details, name='post_details'),
    path('post/new/', views.post_new, name='post_new'),
    path('post_edit/<slug>/<id>/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_drafts_list, name='post_drafts_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<slug>/<id>/remove/', views.post_remove, name='post_remove'),
    path('filter/<int:pk>/', views.post_filter, name='post_filter'),
    # path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('like/', views.post_like, name='like'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]
