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

    def test_should_query_by_age(self):
        response = self.client.get(reverse('likeme:index'), {"age": 30})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

    def test_should_query_by_latitude(self):
        response = self.client.get(reverse('likeme:index'), {"latitude": 40.71667})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

    def test_should_query_by_longitude(self):
        response = self.client.get(reverse('likeme:index'), {"longitude": 40.71667})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

    def test_should_query_by_location(self):
        response = self.client.get(reverse('likeme:index'), {"longitude": 40.71667, "latitude": 40.71667})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

    def test_should_query_by_monthly_income(self):
        response = self.client.get(reverse('likeme:index'), {"monthly income": 5132})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

    def test_should_query_by_experienced(self):
        response = self.client.get(reverse('likeme:index'), {"experienced": True})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"peopleLikeYou": []})

