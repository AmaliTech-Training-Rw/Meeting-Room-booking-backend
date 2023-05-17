from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_model_assert_false(self):
        self.assertFalse(False)
