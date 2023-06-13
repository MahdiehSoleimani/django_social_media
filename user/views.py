from django.shortcuts import render
from .models import Profile, FriendRequest

# Create your views here.
def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, context)

def my_profile(request):
	pro = request.user.profile
	you = pro.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	user_posts = Post.objects.filter(user_name=you)
	friends = pro.friends.all()
