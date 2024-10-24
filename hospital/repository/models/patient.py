from django.db import models
from .person import Person


class Patient(Person):
    BLOOD_TYPES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    country = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    street = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPES)
    insurance = models.BooleanField(default=False)
    emergency_contact = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Patient: {super().__str__()}"

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'