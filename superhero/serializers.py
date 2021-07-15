from rest_framework import serializers
from superhero.models import Superhero

class SuperheroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Superhero
        fields = ('name', 'publisher', 'public', 'created_at', 'updated_at')
