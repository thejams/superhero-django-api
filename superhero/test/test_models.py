from django.test import TestCase
from superhero.models import Superhero


class SuperheroTest(TestCase):
    """Test module for Superhero model"""

    def setUp(self):
        Superhero.objects.create(name="Thor", publisher="Marvel", public=True)
        Superhero.objects.create(name="Batman", publisher="DC", public=False)

    def test_superhero_information(self):
        thor = Superhero.objects.get(name="Thor")
        batman = Superhero.objects.get(name="Batman")
        self.assertEqual(thor.get_information(), "Thor belongs to Marvel")
        self.assertEqual(batman.get_information(), "Batman belongs to DC")
