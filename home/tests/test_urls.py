# from django.test import SimpleTestCase
# from django.urls import reverse, resolve
# from home.views import HomeView, PostDeleteView, PostCreateView


# class TestUrls(SimpleTestCase):
#     def test_home(self):
#         url = reverse('home:home')
#         self.assertEqual(resolve(url).func.view_class, HomeView)

#     def test_detail(self):
#         url = reverse('home:post_delete', args=(4,))
#         self.assertEqual(resolve(url).func.view_class, PostDeleteView)

#     def test_create(self):
#         url = reverse('home:post_create')
#         self.assertEqual(resolve(url).func.view_class, PostCreateView)