from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('like/', views.like, name='post-like'),
    path('post/<int:pk>/update/', views.PostUpdateView, name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('notifications/', views.show_notifications, name='notification'),
	path('user_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
