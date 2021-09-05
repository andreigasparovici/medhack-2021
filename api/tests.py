from http import HTTPStatus

from django.test import TestCase, Client

from .models import Diagnostic, Comorbidity, Person


class RegisterTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Comorbidity.objects.create(name="Comorbidity 1")
        Comorbidity.objects.create(name="Comorbidity3 2")
        Diagnostic.objects.create(name="Diagnostic 1")

    def test_register_missing_data(self):
        c = Client()
        response = c.post('/api/register/',
                          data={
                              "first_name": "First",
                              "last_name": "Last",
                              # Missing email and password
                              "birthday": "2000-01-01",
                              "sex": "female",
                              "height": 170,
                              "weight": 60,
                              "diagnostic": 1,
                              "comorbidities": [1, 2]
                          },
                          content_type='application/json')

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_register_invalid_data(self):
        c = Client()
        response = c.post('/api/register/',
                          data={
                              "first_name": "First",
                              "last_name": "Last",
                              "email": "test123", # invalid email
                              "password": "testpw",
                              "birthday": "2000-01-01",
                              "sex": "female",
                              "height": 170,
                              "weight": 60,
                              "diagnostic": 1,
                              "comorbidities": [1, 2]
                          },
                          content_type='application/json')

        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)

    def test_register_valid_data(self):
        c = Client()
        response = c.post('/api/register/',
                          data={
                              "first_name": "First",
                              "last_name": "Last",
                              "email": "test@test.com",
                              "password": "testpw",
                              "birthday": "2000-01-01",
                              "sex": "female",
                              "height": 170,
                              "weight": 60,
                              "diagnostic": 1,
                              "comorbidities": [1, 2]
                          },
                          content_type='application/json')

        self.assertEqual(HTTPStatus.CREATED, response.status_code)
