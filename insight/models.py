from django.db import models


# Create your models here.
class UserImageCase(models.Model):
    image = models.ImageField()

    userPrompt = models.TextField()

    dateCreated = models.DateField().auto_now_add

    resultPrompt = models.TextField()