from django.test import TestCase
from .models import Profile, FriendRequest
from django.contrib.auth.models import User


# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_creation(self):
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_str(self):
        expected_str = f"Profile for{self.user.username}"
        self.assertEqual(str(self.user.profile), expected_str)

    def test_profile_update(self):
        new_username = 'newusername'
        self.user.username = new_username
        self.user.save()
        self.assertEqual(self.user.profile.user.username, new_username)

    if __name__ == '__main__':
        import django
        django.setup()
        test.main()


class FriendRequestTestCase(TestCase):
    def setUp(self):
        """Create test users"""
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

    def test_friend_request_creation(self):
        """Create a friend request"""
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        self.assertEqual(friend_request.sender, self.sender)
        self.assertEqual(friend_request.receiver, self.receiver)
        self.assertEqual(friend_request.status, FriendRequest.is_mutual_friend)

    def test_accept_friend_request(self):
        """ Create a friend request and accept it"""
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        friend_request.accept()
        self.assertEqual(friend_request.status, FriendRequest.add_friend())
        self.assertIn(self.receiver, self.sender.profile.friends.all())
        self.assertIn(self.sender, self.receiver.profile.friends.all())

    def test_reject_friend_request(self):
        """Create a friend request and reject it"""
        friend_request = FriendRequest.objects.create(sender=self.sender, receiver=self.receiver)
        friend_request.reject()
        self.assertEqual(friend_request.status, FriendRequest.decline())
        self.assertNotIn(self.receiver, self.sender.profile.friends.all())
        self.assertNotIn(self.sender, self.receiver.profile.friends.all())




