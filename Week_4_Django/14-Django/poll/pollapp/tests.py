from django.test import TestCase
from django.urls import reverse


class SimpleViewTest(TestCase):
    def test_simple_view(self):
        response = self.client.get(reverse("simple_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, this is a simple view!")
