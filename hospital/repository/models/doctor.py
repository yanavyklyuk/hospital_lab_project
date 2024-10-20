from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from .specialisation import Specialisation
from .person import Person


class Doctor(Person):
    practice_start_date = models.DateField(default=timezone.now)
    specialisation = models.ForeignKey(Specialisation, on_delete=models.RESTRICT)
    education = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='media/doctors/', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def clean(self):
        if self.practice_start_date >= timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'