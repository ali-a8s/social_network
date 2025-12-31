from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import UserRegistrationView, UserLoginView, UserProfileView


class TestUrls(SimpleTestCase):
    def test_register(self):
        url = reverse('accounts:user_register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_login(self):
        url = reverse('accounts:user_login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_profil(self):
        url = reverse('accounts:user_profile', args=(1,))
        self.assertEqual(resolve(url).func.view_class, UserProfileView)    