from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse

# Create your tests here.


class LikeMeIndexTests(TestCase):

    def test_should_return_json(self):
        response = self.client.get(reverse('likeme:index'))
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        print(type(response.content))
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})
