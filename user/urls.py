from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView, EditUserView, UserUnfollowView, UserFollowView, \
    UserProfileView, ProfileListView, CancelFriendRequest, SearchUsers, ProfileUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view, name='register'),
    path('login/', UserLoginView.as_view, name='login'),
    path('logout/', UserLogoutView.as_view, name='logout'),
    path('edit_user/', EditUserView.as_view, name='edit_user'),
    path('profile_list/', ProfileListView.as_view, name='profile_list'),
    path('cancel_request/', CancelFriendRequest.as_view, name='cancel_request'),
    path('follow/<int:user_id>/', UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', UserUnfollowView.as_view(), name='user_unfollow'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('search_user/', SearchUsers.as_view(), name='search_user'),
    path('profile_update/<int:user_id>/', ProfileUpdateView.as_view(), name='update_profile'),

]
