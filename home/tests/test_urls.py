from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home import views


class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse('home:home')
        self.assertEqual(resolve(url).func.view_class, views.HomeView)

    def test_post_detail(self):
        url = reverse('home:post_detail', args=(1, 'one'))
        self.assertEqual(resolve(url).func.view_class, views.PostDetailView)

    def test_post_create(self):
        url = reverse('home:post_create')
        self.assertEqual(resolve(url).func.view_class, views.PostCreateView)
    
    def test_post_update(self):
        url = reverse('home:post_update', args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.PostUpdateView)

    def test_post_delete(self):
        url = reverse('home:post_delete', args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.PostDeleteView)
    
    def test_like(self):
        url = reverse('home:post_like', args=(1,))
        self.assertEqual(resolve(url).func.view_class, views.PostLikeView)