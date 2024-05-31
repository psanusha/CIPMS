
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class userdetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()

    def __str__(self):
        return f'{self.user.username} - {self.email}'