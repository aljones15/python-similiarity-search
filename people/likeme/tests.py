from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse

# Create your tests here.


class LikeMeIndexTests(TestCase):

    def test_should_return_json(self):
        response = self.client.get(reverse('likeme:index'))
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

    def test_should_query_by_name(self):
        response = self.client.get(reverse('likeme:index'), {"name": "Kendra"})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

