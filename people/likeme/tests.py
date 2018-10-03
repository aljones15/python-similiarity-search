from math import isclose
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .views import getDataFrame
from .transform import topTen

# Create your tests here.

df = getDataFrame()
topDefault = {'peopleLikeYou': topTen(df)}

class LikeMeIndexTests(TestCase):

    def test_should_return_json(self):
        response = self.client.get(reverse('likeme:index'))
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), topDefault)

    def test_should_query_by_name(self):
        response = self.client.get(reverse('likeme:index'), {"name": "Kendra"})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)

    def test_should_query_by_age(self):
        response = self.client.get(reverse('likeme:index'), {"age": 30})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), topDefault)

    def test_should_query_by_latitude(self):
        latitude = 40.71667
        response = self.client.get(reverse('likeme:index'), {"latitude": latitude})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLatitude = json[0]['latitude']
        self.assertEqual(latitude, actualLatitude) 

    def test_should_query_by_longitude(self):
        longitude = 59.6818456
        response = self.client.get(reverse('likeme:index'), {"longitude": longitude})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(longitude, actualLongitude)

    def test_should_query_by_location(self):
        latitude = 44.8501354
        longitude = -0.5702805
        response = self.client.get(reverse('likeme:index'), {"longitude": longitude, "latitude": latitude})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actualLongitude),True,'asserted longitudes would match')
        actualLatitude = json[0]['latitude']
        self.assertEqual(latitude, actualLatitude, 'asserted that latitudes would match') 

    def test_should_query_by_monthly_income(self):
        response = self.client.get(reverse('likeme:index'), {"monthly income": 5132})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), topDefault)

    def test_should_query_by_experienced_True(self):
        response = self.client.get(reverse('likeme:index'), {"experienced": True})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)

    def test_should_query_by_experienced_False(self):
        response = self.client.get(reverse('likeme:index'), {"experienced": False})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)

# TODO add validation checks for each function

