import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from superhero.models import Superhero
from superhero import serializers


# initialize the APIClient app
client = Client()

class GetAllSuperheroesTest(TestCase):
    """ Test module for GET all puppies API """
    serializer_class = serializers.SuperheroSerializer

    def setUp(self):
        Superhero.objects.create(name='Thor', publisher='Marvel', public=True)
        Superhero.objects.create(name='Batman', publisher='DC', public=True)
        Superhero.objects.create(name='Iron Man', publisher='Marvel', public=False)
        Superhero.objects.create(name='Superman', publisher='DC', public=False)

    def test_get_all_puppies(self):
        # get API response
        response = client.get(reverse('get_post_superheroes'))
        # get data from db
        superheroes = Superhero.objects.all()
        serializer = self.serializer_class(superheroes, many=True)
        self.assertEqual(response.data, {'superheroes': serializer.data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSingleSuperheroTest(TestCase):
    """ Test module for GET single superhero API """
    serializer_class = serializers.SuperheroSerializer

    def setUp(self):
        self.loki = Superhero.objects.create(name='Loki', publisher='Marvel', public=True)
        self.joker = Superhero.objects.create(name='The Joker', publisher='DC', public=True)
        self.thanos = Superhero.objects.create(name='Thanos', publisher='Marvel', public=False)
        self.lex = Superhero.objects.create(name='Lex Luthor', publisher='DC', public=False)

    def test_get_valid_single_superhero(self):
        response = client.get(reverse('get_delete_put_single_superhero', kwargs={'id': self.loki.pk}))
        superhero = Superhero.objects.get(pk=self.loki.pk)
        serializer = self.serializer_class(superhero)
        self.assertEqual(response.data, {'superhero': serializer.data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_superhero(self):
        response = client.get(reverse('get_delete_put_single_superhero', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewSuperHeroTest(TestCase):
    """ Test module for inserting a new superhero """

    def setUp(self):
        self.valid_payload = {
            "name": "Judas Priest",
            "publisher": "Marvel",
            "public": True
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'publisher': 'DC'
        }

    def test_create_valid_superhero(self):
        response = client.post(
            reverse('get_post_superheroes'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_superhero(self):
        response = client.post(
            reverse('get_post_superheroes'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleSuperheroTest(TestCase):
    """ Test module for updating an existing superhero record """

    def setUp(self):
        self.darkseid = Superhero.objects.create(name='Darkseid', publisher='DC', public=True)
        self.kang = Superhero.objects.create(name='Kang The Conqueror', publisher='Marvel', public=True)
        self.valid_payload = {
            "name": "Judas Priest",
            "publisher": "Marvel",
            "public": True
        }
        self.invalid_payload = {
            'name': '',
            'age': 4,
            'publisher': 'DC'
        }

    def test_valid_update_superhero(self):
        response = client.put(
            reverse('get_delete_put_single_superhero', kwargs={'id': self.darkseid.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_superhero(self):
        response = client.put(
            reverse('get_delete_put_single_superhero', kwargs={'id': self.kang.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleSuperheroTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.deadpool = Superhero.objects.create(name='Deadpool', publisher='Marvel', public=True)
        self.reverse_flash = Superhero.objects.create(name='Reverse Flash', publisher='DC', public=True)

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_put_single_superhero', kwargs={'id': self.deadpool.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_put_single_superhero', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)