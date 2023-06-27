from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, Reaction


class PostTestCase(TestCase):
    def setUp(self):
        """
        Create a test user
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    fieldsets = (
        (
            None, {
                'fields': ('text', ('user', 'status', 'is_deleted'), 'tags'),
            },
        ),
    )
    
    def test_post_creation(self):
        """
        Create a post
        """
        post = Post.objects.create(author=self.user, content='Test post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, 'Test post')

    def test_post_str(self):
        """
        Check if the post's __str__ method returns the expected string representation
        """
        post = Post.objects.create(author=self.user, content='Test post')
        expected_str = f"Post by {self.user.username}"
        self.assertEqual(str(post), expected_str)

    def test_post_update(self):
        """
        Update the post and check if the changes are reflected
        """
        post = Post.objects.create(author=self.user, content='Test post')
        new_content = 'Updated post'
        post.content = new_content
        post.save()
        updated_post = Post.objects.get(pk=post.pk)
        self.assertEqual(updated_post.content, new_content)


class CommentTestCase(TestCase):
    def setUp(self):
        """"Create a test user"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        """Create a test post"""
        self.post = Post.objects.create(author=self.user, content='Test post')

    def test_get_replies(self):
        """
        Create a comment and its replies
        Get the replies for the comment
        """
        comment = Comment.objects.create(post=self.post, user=self.user, comment='Test comment')
        reply1 = Comment.objects.create(post=self.post, user=self.user, comment='Reply 1', reply=comment)
        reply2 = Comment.objects.create(post=self.post, user=self.user, comment='Reply 2', reply=comment)

        replies = comment.get_replies()
        self.assertEqual(len(replies), 2)
        self.assertIn(reply1, replies)
        self.assertIn(reply2, replies)

    def test_add_reply(self):
        """Create a comment"""
        comment = Comment.objects.create(post=self.post, user=self.user, comment='Test comment')

        """Add a reply"""
        reply_user = User.objects.create_user(username='replyuser', password='replypassword')
        reply_content = 'Reply to comment'
        reply = comment.add_reply(reply_user, reply_content)

        """Assert the reply is created correctly"""
        self.assertEqual(reply.post, self.post)
        self.assertEqual(reply.user, reply_user)
        self.assertEqual(reply.comment, reply_content)
        self.assertEqual(reply.reply, comment)

    def test_delete_comment(self):
        """ Create a comment and its replies"""
        comment = Comment.objects.create(post=self.post, user=self.user, comment='Test comment')
        reply1 = Comment.objects.create(post=self.post, user=self.user, comment='Reply 1', reply=comment)
        reply2 = Comment.objects.create(post=self.post, user=self.user, comment='Reply 2', reply=comment)

        """Delete the comment and its replies"""
        comment.delete_comment()

        """Check if the comment and its replies are deleted"""
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
        self.assertFalse(Comment.objects.filter(pk=reply1.pk).exists())
        self.assertFalse(Comment.objects.filter(pk=reply2.pk).exists())


class TagTestCase(TestCase):
    def setUp(self):
        """Create test posts"""
        self.post1 = Post.objects.create(author=None, content='Post 1')
        self.post2 = Post.objects.create(author=None, content='Post 2')

    def test_get_posts(self):
        """
        Create a tag and associate it with posts
        Get the posts associated with the tag
        """
        tag = Tag.objects.create(text='Test Tag')
        tag.post.add(self.post1, self.post2)

        posts = tag.get_posts()
        self.assertEqual(posts.count(), 2)
        self.assertIn(self.post1, posts)
        self.assertIn(self.post2, posts)

    def test_add_post(self):
        """Create a tag"""
        tag = Tag.objects.create(text='Test Tag')

        """Associate a post with the tag"""
        tag.add_post(self.post1)

        """Check if the post is associated with the tag"""
        self.assertEqual(tag.post.count(), 1)
        self.assertIn(self.post1, tag.post.all())

    def test_remove_post(self):
        """Create a tag and associate posts with it"""
        tag = Tag.objects.create(text='Test Tag')
        tag.post.add(self.post1, self.post2)

        # Remove a post from the tag
        tag.remove_post(self.post1)

        # Check if the post is no longer associated with the tag
        self.assertEqual(tag.post.count(), 1)
        self.assertNotIn(self.post1, tag.post.all())

    def test_get_post_count(self):
        """Create a tag and associate posts with it
        Get the post count for the tag
        """
        tag = Tag.objects.create(text='Test Tag')
        tag.post.add(self.post1, self.post2)

        post_count = tag.get_post_count()
        self.assertEqual(post_count, 2)

    def test_is_used(self):
        """Create a tag"""
        tag = Tag.objects.create(text='Test Tag')

        # Initially, the tag should not be used
        self.assertFalse(tag.is_used())

        # Associate a post with the tag
        tag.add_post(self.post1)
        self.assertTrue(tag.is_used())


class ReactionTestCase(TestCase):
    def setUp(self):
        """
        Create test users
        Create a test post
        Create a test reaction
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.post = Post.objects.create(title='Test Post', content='Lorem ipsum dolor sit amet')

        self.reaction = Reaction.objects.create(user=self.user, post=self.post, status=None)

    def test_like_reaction(self):
        """
        Like the reaction
        Retrieve the reaction from the database
        Assert that the reaction status is now True
        """
        self.reaction.like()
        updated_reaction = Reaction.objects.get(id=self.reaction.id)
        self.assertTrue(updated_reaction.status)

    def test_is_liked(self):
        """
        Like the reaction
        Check if the reaction is liked
         """
        self.reaction.like()
        is_liked = self.reaction.is_liked()
        self.assertTrue(is_liked)

    def test_is_unliked(self):
        """Unlike the reaction
        Check if the reaction is unliked"""
        self.reaction.unlike()
        is_unliked = self.reaction.is_unliked()
        self.assertTrue(is_unliked)

    def test_remove_reaction(self):
        """
        Remove the reaction
        Retrieve the reaction from the database
        Assert that the reaction status is now None
        """
        self.reaction.remove_reaction()
        updated_reaction = Reaction.objects.get(id=self.reaction.id)
        self.assertIsNone(updated_reaction.status)

    def test_update_reaction(self):
        """
        Update the reaction status to True
        Retrieve the reaction from the database
        Assert that the reaction status is now True
        """
        self.reaction.update_reaction(True)
        updated_reaction = Reaction.objects.get(id=self.reaction.id)
        self.assertTrue(updated_reaction.status)

