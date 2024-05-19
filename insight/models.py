from django.db import models


# Create your models here.
class UserImageCase(models.Model):
    image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=255, null=True)
    resultPrompt = models.TextField(null=True)