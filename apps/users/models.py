from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pricture = models.ImageField(upload_to ='profile_pictures/', blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    