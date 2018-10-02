from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class LikeMeIndexTests(TestCase):

    def test_should_return_json(self):
        response = self.client.get(reverse('likeme:index'))
        self.assertIs(response.status_code, 200);
