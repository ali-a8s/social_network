from django.test import TestCase
from home.forms import PostCreateUpdateForm, PostSearchForm, CommenCreateForm


class TestPostCreateUpdateForm(TestCase):
    def test_valid_data(self):
        form = PostCreateUpdateForm(data={'title': 'test one',
                                          'body': 'this body test one'})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = PostCreateUpdateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)