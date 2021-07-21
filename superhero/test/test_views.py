import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from superhero.models import Superhero
from superhero import serializers


class SuperheroViewsTest(TestCase):
    """Test module for GET all puppies API"""

    def setUp(self):
        self.serializer_class = serializers.SuperheroSerializer
        self.client = Client()

        Superhero.objects.create(name="Thor", publisher="Marvel", public=True)
        Superhero.objects.create(name="Batman", publisher="DC", public=True)
        Superhero.objects.create(
            name="Iron Man",
            publisher="Marvel",
            public=False,
        )
        Superhero.objects.create(name="Superman", publisher="DC", public=False)

        self.loki = Superhero.objects.create(
            name="Loki", publisher="Marvel", public=True
        )
        self.darkseid = Superhero.objects.create(
            name="Darkseid", publisher="DC", public=True
        )
        self.kang = Superhero.objects.create(
            name="Kang The Conqueror", publisher="Marvel", public=True
        )
        self.deadpool = Superhero.objects.create(
            name="Deadpool", publisher="Marvel", public=True
        )

        self.valid_payload = {
            "name": "Judas Priest",
            "publisher": "Marvel",
            "public": True,
        }
        self.invalid_payload = {"name": "", "age": 4, "publisher": "DC"}

    def test_get_all_superheroes(self):
        # TEST GET ALL SUPERHEROES VIEW
        response = self.client.get(reverse("get_post_superheroes"))
        superheroes = Superhero.objects.all()
        serializer = self.serializer_class(superheroes, many=True)

        self.assertEqual(response.data, {"superheroes": serializer.data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_superhero(self):
        # TEST GET SINGLE SUPERHERO VIEW
        response = self.client.get(
            reverse(
                "get_delete_put_single_superhero",
                kwargs={"id": self.loki.pk},
            )
        )
        superhero = Superhero.objects.get(pk=self.loki.pk)
        serializer = self.serializer_class(superhero)

        self.assertEqual(response.data, {"superhero": serializer.data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_superhero(self):
        # TEST GET 204 IN SINGLE GET SINGLE SUPERHERO VIEW
        response = self.client.get(
            reverse("get_delete_put_single_superhero", kwargs={"id": 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_superhero(self):
        # TEST POST SUPERHERO VIEW
        response = self.client.post(
            reverse("get_post_superheroes"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_superhero(self):
        # TEST ERROR IN POST SUPERHERO VIEW
        response = self.client.post(
            reverse("get_post_superheroes"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_update_superhero(self):
        # TEST UPDATE SUPERHERO VIEW
        response = self.client.put(
            reverse(
                "get_delete_put_single_superhero",
                kwargs={"id": self.darkseid.pk},
            ),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_superhero(self):
        # TEST ERROR IN UPDATE SUPERHERO VIEW
        response = self.client.put(
            reverse(
                "get_delete_put_single_superhero",
                kwargs={"id": self.kang.pk},
            ),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_puppy(self):
        # TEST DELETE SUPERHERO VIEW
        response = self.client.delete(
            reverse(
                "get_delete_put_single_superhero",
                kwargs={"id": self.deadpool.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        # TEST ERROR IN DELETE SUPERHERO VIEW
        response = self.client.delete(
            reverse("get_delete_put_single_superhero", kwargs={"id": 30})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
