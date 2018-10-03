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
        name = "Kendra"
        response = self.client.get(reverse('likeme:index'), {"name": name})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualName = json[0]['name']
        self.assertEqual(name, actualName) 

    def test_should_query_by_age(self):
        age = 30
        response = self.client.get(reverse('likeme:index'), {"age": age})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualAge = json[0]['age']
        self.assertEqual(age, actualAge) 

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
        income = 5132
        response = self.client.get(reverse('likeme:index'), {"monthly income": income})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualIncome = json[0]['monthly income']
        self.assertEqual(income, actualIncome,'asserted incomes would match')

    def test_should_query_by_monthlyIncome(self):
        income = 5132
        response = self.client.get(reverse('likeme:index'), {"monthlyIncome": income})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualIncome = json[0]['monthly income']
        self.assertEqual(income, actualIncome,'asserted incomes would match')

    def test_should_query_by_experienced_True(self):
        response = self.client.get(reverse('likeme:index'), {"experienced": True})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualExp = json[0]['experienced']
        self.assertEqual(True, actualExp)

    def test_should_query_by_experienced_False(self):
        response = self.client.get(reverse('likeme:index'), {"experienced": False})
        self.assertIs(response.status_code, 200)
        self.assertIs(type(response), JsonResponse)
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualExp = json[0]['experienced']
        self.assertEqual(False, actualExp)

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
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actualLongitude),True,'asserted longitudes would match')
        actualLatitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actualLatitude),True, 'asserted that latitudes would match') 
        actualAge = json[0]['age']
        self.assertEqual(age, actualAge) 

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
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actualLongitude),True,'asserted longitudes would match')
        actualLatitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actualLatitude),True, 'asserted that latitudes would match') 
        actualAge = json[0]['age']
        self.assertEqual(age, actualAge) 
        actualIncome = json[0]['monthly income']
        self.assertEqual(income, actualIncome) 

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
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actualLongitude),True,'asserted longitudes would match')
        actualLatitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actualLatitude),True, 'asserted that latitudes would match') 
        actualAge = json[0]['age']
        self.assertEqual(age, actualAge) 
        actualIncome = json[0]['monthly income']
        self.assertEqual(income, actualIncome) 
        actualName = json[0]['name']
        self.assertEqual(name, actualName) 

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
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actualLongitude),True,'asserted longitudes would match')
        actualLatitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actualLatitude),True, 'asserted that latitudes would match') 
        actualAge = json[0]['age']
        self.assertEqual(age, actualAge) 
        actualIncome = json[0]['monthly income']
        self.assertEqual(income, actualIncome) 
        actualName = json[0]['name']
        self.assertEqual(name, actualName)
        actualExp = json[0]['experienced']
        self.assertEqual(False, actualExp)

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
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), topDefault)
        json = response.json()['peopleLikeYou']
        actualLongitude = json[0]['longitude']
        self.assertEqual(isclose(longitude, actualLongitude),True,'asserted longitudes would match')
        actualLatitude = json[0]['latitude']
        self.assertEqual(isclose(latitude, actualLatitude),True, 'asserted that latitudes would match') 
        actualAge = json[0]['age']
        self.assertEqual(age, actualAge) 
        actualIncome = json[0]['monthly income']
        self.assertEqual(income, actualIncome) 
        actualName = json[0]['name']
        self.assertEqual(name, actualName)
        actualExp = json[0]['experienced']
        self.assertEqual(False, actualExp)
