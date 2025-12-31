from django.test import TestCase
from accounts.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='kevin',
                                 email='kevin@email.com',
                                 password='kevin')

    def test_valid_data(self):
        form = UserRegistrationForm(data={'username':'jack',
                                          'email':'jack@email.com',
                                          'password1': 'jack',
                                          'password2':'jack'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exists_email(self):
        form = UserRegistrationForm(data={'username':'not_kev',
                                          'email':'kevin@email.com',
                                          'password1': 'kevin',
                                          'password2':'kevin'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email'))

    def test_on_match_password(self):
        form = UserRegistrationForm(data={'username':'mark',
                                          'email':'mark@email.com',
                                          'password1': 'mark',
                                          'password2':'kevin'})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
        
        