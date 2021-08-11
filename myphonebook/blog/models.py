from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    address = models.CharField(max_length = 255)
    name = models.ForeignKey(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length=12)
    

    def __str__(self):
        return f'{self.address} | {self.name}'