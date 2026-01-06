from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from home.models import Post  
from home.forms import PostCreateUpdateForm, PostSearchForm


class TestHomeView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertIsInstance(response.context['form'],
                              PostSearchForm)


class TestPostCreateView(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_post_create_GET(self):
        response = self.client.get(reverse('home:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/create.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], PostCreateUpdateForm)
    
    def test_post_create_POST(self):
        response = self.client.post(
            reverse('home:post_create'),
            data={'title': 'title test', 'body': 'body test'}
        )
        self.assertEqual(response.status_code, 302)
        new_post = Post.objects.first()
        if new_post:
            self.assertRedirects(
                response, 
                reverse('home:post_detail', args=[new_post.id, new_post.slug])
            )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, 'title test')
        self.assertEqual(Post.objects.first().user, self.user)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'you created a new post')
    
    def test_post_create_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('home:post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/') or 
                       response.url.startswith('/login/'))