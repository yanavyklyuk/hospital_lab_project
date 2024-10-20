from django.db import models
from django.utils import timezone
from .specialisation import Specialisation
from .person import Person


class Doctor(Person):
    practice_start_date = models.DateField(default=timezone.now)
    specialisation = models.ForeignKey(Specialisation, on_delete=models.CASCADE)
    education = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='media/doctors/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
