from django.test import TestCase, Client
from django.urls import reverse
from accounts.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse('accounts:user_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], 
                              UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(reverse('accounts:user_register'), 
                                    data={'username':'jack',
                                          'email':'jack@email.com',
                                          'password1': 'jack',
                                          'password2':'jack'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home:home'))
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('accounts:user_register'), 
                                    data={'username':'jack',
                                          'email':'invalid email',
                                          'password1': 'jack',
                                          'password2':'jack'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'],
                             field='email', 
                             errors=['Enter a valid email address.'])
        

class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='root', 
                          email='root@email.com',
                          password='root')
        self.client = Client()
        self.client.login(username='root', 
                          email='root@email.com',
                          password='root')
        
    def test_profile(self):
        response = self.client.get(reverse('accounts:user_profile', args=(self.user.id, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')  