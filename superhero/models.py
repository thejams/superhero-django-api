from django.db import models

# Create your models here.
class Superhero(models.Model):
    name = models.CharField(max_length=100)
    publisher =  models.CharField(max_length=100)
    public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_information(self):
        return self.name + ' belongs to ' + self.publisher