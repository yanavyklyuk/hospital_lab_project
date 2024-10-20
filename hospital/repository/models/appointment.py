from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from .doctor import Doctor
from .patient import Patient
from .favor import Favor

class Appointment(models.Model):
    datetime_of_appointment = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('scheduled', 'Scheduled'), ('happened', 'Happened'),
                                                      ('cancelled', 'Cancelled')], default = 'scheduled')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.RESTRICT)
    favor = models.ForeignKey(Favor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.datetime_of_appointment} - {self.patient} - {self.doctor}"

    def clean(self):
        if self.datetime_of_appointment <= timezone.now():
            raise ValidationError("Appointment cannot be in the past.")

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-datetime_of_appointment']
        constraints = [
            models.UniqueConstraint(fields=['datetime_of_appointment', 'patient'], name = 'uq_date_patient'),
            models.UniqueConstraint(fields=['datetime_of_appointment', 'doctor'], name = 'uq_date_doctor'),
        ]