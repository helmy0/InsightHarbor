from django.db import models
from django.forms import fields
from .models import UserImageCase
from django import forms


class InsightRequest(forms.ModelForm):

    class Meta:

        model = UserImageCase

        fields = ['image', 'resultPrompt']



