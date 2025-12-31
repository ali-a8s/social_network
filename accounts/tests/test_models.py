from django.test import TestCase
from accounts.models import Relation
from django.contrib.auth.models import User


class TestRelationModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.kevin = User.objects.create_user(username='kevin',
                                 email='kevin@email.com',
                                 password='kevin')
        cls.jack = User.objects.create_user(username='jack',
                                 email='jack@email.com',
                                 password='jack')

    def test_model_str(self):
        relation = Relation.objects.create(from_user=self.kevin,
                                           to_user=self.jack)
        self.assertEqual(str(relation), 'kevin following jack')