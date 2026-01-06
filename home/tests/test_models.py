from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from home.models import Post, Comment, Vote

class TestPostModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123')
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post Title',
            body='Test post content for testing purposes',
            slug='test-post-title')
    
    def test_str_post(self):
        self.assertEqual(str(self.post), 
                         f'{self.user} posted {self.post.title}')
    
    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), 
                         reverse("home:post_detail", args=[self.post.id, self.post.slug]))
    
    def test_likes_count(self):
        count = self.post.likes_count()
        self.assertEqual(count, 0)
    
    def test_user_can_like(self):
        new_user = User.objects.create_user(username='newuser',
                                            password='testpass123')

        can_like = self.post.user_can_like(new_user)
        self.assertFalse(can_like)


class TestCommentModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123')
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post Title',
            body='Test post content for testing purposes',
            slug='test-post-title')
        self.comment = Comment(user = self.user,
                               post = self.post,
                               body = 'test comment')
        
    def test_str_comment(self):
        self.assertEqual(str(self.comment),
                         f'{self.comment.user} commented on {self.comment.post}')
        
    
class TestVoteModel(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123')
        self.post = Post.objects.create(
            user=self.user,
            title='Test Post Title',
            body='Test post content for testing purposes',
            slug='test-post-title')
        self.vote = Vote(user = self.user,
                               post = self.post)
        self.vote.save()
        
    def test_str_vote(self):
        self.assertEqual(str(self.vote), 
                         f'{self.vote.user} liked {self.vote.post}')
        
    def test_likes_count(self):
        count = self.post.likes_count()
        self.assertEqual(count, 1)