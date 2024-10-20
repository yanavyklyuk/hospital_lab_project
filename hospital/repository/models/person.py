from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_birth = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if self.date_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
