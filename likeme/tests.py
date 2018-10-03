from math import isclose
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .views import getDataFrame
from .transform import top_ten

# Create your tests here.

DATA_FRAME = getDataFrame()
TOP_DEFAULT = {'peopleLikeYou': top_ten(DATA_FRAME)}

class LikeMeIndexTests(TestCase):
    "LikeMeIndexTests is the default test project for the people-like-me route"

    def test_should_return_json(self):
        "the route should at the least return json matching the default sort order"
        response = self.client.get(reverse('likeme:index'))
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)

    def test_should_query_by_name(self):
        "here we look for Kendra and make sure that the first highest score result matches her name"
        name = "Kendra"
        response = self.client.get(reverse('likeme:index'), {"name": name})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_name = json[0]['name']
        self.assertEqual(name, actual_name)

    def test_should_query_by_age(self):
        "search by age and test that the top result matches the age put in"
        age = 30
        response = self.client.get(reverse('likeme:index'), {"age": age})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_age = json[0]['age']
        self.assertEqual(age, actual_age)

    def test_should_return_empty_if_not_confident(self):
        "if the probability is less than 0.4 do not return anything"
        age = 1000
        response = self.client.get(reverse('likeme:index'), {"age": age})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        self.assertEqual(len(json), 0, 'expected no results')


    def test_should_query_by_latitude(self):
        "latitude query with test that the top result matches"
        latitude = 40.71667
        response = self.client.get(reverse('likeme:index'), {"latitude": latitude})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_latitude = json[0]['latitude']
        self.assertEqual(latitude, actual_latitude)

    def test_should_query_by_longitude(self):
        "tests that the top result matches the exact longitude given"
        longitude = 59.6818456
        response = self.client.get(reverse('likeme:index'), {"longitude": longitude})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(longitude, actual_longitude)

    def test_should_query_by_location(self):
        "this is to ensure that when searching by both longitude & latitude we don't skew the results"
        latitude = 44.8501354
        longitude = -0.5702805
        response = self.client.get(reverse('likeme:index'), {"longitude": longitude, "latitude": latitude})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actual_longitude), True, 'asserted longitudes would match')
        actual_latitude = json[0]['latitude']
        self.assertEqual(latitude, actual_latitude, 'asserted that latitudes would match')

    def test_should_query_by_monthly_income(self):
        "test that monthly income returns the correct results"
        income = 5132
        response = self.client.get(reverse('likeme:index'), {"monthly income": income})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_income = json[0]['monthly income']
        self.assertEqual(income, actual_income, 'asserted incomes would match')

    def test_should_query_by_monthlyIncome(self):
        "monthlyIncome can also be camel cased so we test that functionality works too"
        income = 5132
        response = self.client.get(reverse('likeme:index'), {"monthlyIncome": income})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_income = json[0]['monthly income']
        self.assertEqual(income, actual_income, 'asserted incomes would match')

    def test_should_query_by_experienced_True(self):
        "make sure that the top result has experienced True"
        response = self.client.get(reverse('likeme:index'), {"experienced": True})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_experience = json[0]['experienced']
        self.assertEqual(True, actual_experience)

    def test_should_query_by_experienced_False(self):
        "make sure the top result has experienced False"
        response = self.client.get(reverse('likeme:index'), {"experienced": False})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_experience = json[0]['experienced']
        self.assertEqual(False, actual_experience)

    def test_should_query_on_three_fields(self):
        # Branden,67,-7.1765737,111.3828738,4681,false
        age = 67
        latitude = -7.1765737
        longitude = 111.3828738
        query = {
            'age': age,
            'latitude': latitude,
            'longitude': longitude
        }
        response = self.client.get(reverse('likeme:index'), query)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actual_longitude), True, 'asserted longitudes would match')
        actual_latitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actual_latitude), True, 'asserted that latitudes would match') 
        actual_age = json[0]['age']
        self.assertEqual(age, actual_age) 

    def test_should_query_on_four_fields(self):
        # Glynis,70,27.756647,118.035309,14424,true
        age = 70
        latitude = 27.756647
        longitude = 118.035309
        income = 14424
        query = {
            'age': age,
            'latitude': latitude,
            'longitude': longitude,
            'income': income
        }
        response = self.client.get(reverse('likeme:index'), query)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actual_longitude), True, 'asserted longitudes would match')
        actual_latitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actual_latitude), True, 'asserted that latitudes would match') 
        actual_age = json[0]['age']
        self.assertEqual(age, actual_age) 
        actual_income = json[0]['monthly income']
        self.assertEqual(income, actual_income) 

    def test_should_query_on_five_fields(self):
        # Jay,92,-22.9916783,-45.5651683,3476,true
        age = 92
        latitude = -22.9916783
        longitude = -45.5651683
        income = 3476
        name = "Jay"
        query = {
            'name': name,
            'age': age,
            'latitude': latitude,
            'longitude': longitude,
            'income': income
        }
        response = self.client.get(reverse('likeme:index'), query)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actual_longitude), True, 'asserted longitudes would match')
        actual_latitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actual_latitude), True, 'asserted that latitudes would match') 
        actual_age = json[0]['age']
        self.assertEqual(age, actual_age) 
        actual_income = json[0]['monthly income']
        self.assertEqual(income, actual_income) 
        actual_name = json[0]['name']
        self.assertEqual(name, actual_name) 

    def test_should_query_on_six_fields(self):
        # Lexis,80,0.5128922,-77.2864879,3839,false
        age = 80
        latitude = 0.5128922
        longitude = -77.2864879
        income = 3839
        name = "Lexis"
        experienced = "false"
        query = {
            'name': name,
            'age': age,
            'latitude': latitude,
            'longitude': longitude,
            'income': income,
            'experienced': experienced
        }
        response = self.client.get(reverse('likeme:index'), query)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actual_longitude), True, 'asserted longitudes would match')
        actual_latitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actual_latitude), True, 'asserted that latitudes would match') 
        actual_age = json[0]['age']
        self.assertEqual(age, actual_age) 
        actual_income = json[0]['monthly income']
        self.assertEqual(income, actual_income) 
        actual_name = json[0]['name']
        self.assertEqual(name, actual_name)
        actual_experience = json[0]['experienced']
        self.assertEqual(False, actual_experience)

    def test_should_ignore_extra_fields(self):
        # Lexis,80,0.5128922,-77.2864879,3839,false
        age = 80
        latitude = 0.5128922
        longitude = -77.2864879
        income = 3839
        name = "Lexis"
        experienced = "false"
        query = {
            'name': name,
            'age': age,
            'latitude': latitude,
            'longitude': longitude,
            'income': income,
            'experienced': experienced,
            'extra': 'field',
            'more': 'fields'
        }
        response = self.client.get(reverse('likeme:index'), query)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), TOP_DEFAULT)
        json = response.json()['peopleLikeYou']
        actual_longitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actual_longitude), True, 'asserted longitudes would match')
        actual_latitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actual_latitude), True, 'asserted that latitudes would match') 
        actual_age = json[0]['age']
        self.assertEqual(age, actual_age) 
        actual_income = json[0]['monthly income']
        self.assertEqual(income, actual_income) 
        actual_name = json[0]['name']
        self.assertEqual(name, actual_name)
        actual_experience = json[0]['experienced']
        self.assertEqual(False, actual_experience)
