from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import PostListView, PostUpdateView, PostAddReplyView, CommentView, CommentEdit, PostLikeView

urlpatterns = {
                  path('post/<int:pk>/update/', PostUpdateView.as_view, name='post-update'),
                  path('post/<int:pk>/reply/', PostAddReplyView.as_view, name='reply_post'),
                  path('search_posts/', views.SearchPost, name='search_posts'),
                  path('comment/', CommentView.as_view, name='comment'),
                  path('edit/comment/', CommentEdit.as_view, name='edit_comment'),
                  path('post/new/', views.PostCreateView, name='post-create'),
                  path('post/<int:pk>/', views.PostDetailView, name='post-detail'),
                  path('user_posts/<str:username>', PostListView.as_view(), name='user-posts'),
                  path('notifications/', views.NotificationListView, name='notification'),
                  path('like_comment/', PostLikeView.as_view, name='like_post'),
                  path('tag/', views.TagListView, name='tag'),
                  path('tag/post/', views.TagDetailView, name='detail_tag'),
                  path('room/', views.RoomListView, name='room'),



              } \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
