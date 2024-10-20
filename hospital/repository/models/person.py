from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    date_birth = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
