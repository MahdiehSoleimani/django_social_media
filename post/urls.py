from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PostListView, PostDeleteView, PostUpdateView

urlpatterns = {
                  path('post/<int:pk>/update/', PostUpdateView.as_view, name='post-update'),
                  path('post/<int:pk>/delete/', PostDeleteView.as_view, name='post-delete'),
                  path('search_posts/', views.SearchPost, name='search_posts'),
                  path('post/new/', views.PostCreateView, name='post-create'),
                  path('post/<int:pk>/', views.PostDetailView, name='post-detail'),
                  path('user_posts/<str:username>', PostListView.as_view(), name='user-posts'),
                  path('notifications/', views.Notification, name='notification'),
              } \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
