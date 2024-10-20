from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from .disease import Disease
from .patient import Patient
from .doctor import Doctor


class DiseaseHistory(models.Model):
    start_of_disease = models.DateField()
    end_of_disease = models.DateField(null = True, blank = True)
    patient = models.ForeignKey(Patient, on_delete = models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete = models.SET_NULL, null = True)
    disease = models.ForeignKey(Disease, on_delete = models.RESTRICT)

    def __str__(self):
        return f"Disease history: {self.patient} - {self.disease} - {self.start_of_disease} -  {self.end_of_disease}"

    def clean(self):
        if self.start_of_disease > timezone.now().date():
            raise ValidationError("Start date cannot be in the future.")

        if self.end_of_disease and self.end_of_disease > timezone.now().date():
            raise ValidationError("End date cannot be in the future.")

        if self.end_of_disease and self.end_of_disease <= self.start_of_disease:
            raise ValidationError("End date must be greater than start date.")

    class Meta:
        verbose_name = "Disease history"
        verbose_name_plural = "Diseases history"
        ordering = ['-start_of_disease']
        constraints = [
            models.CheckConstraint(check = Q(end_of_disease__gt=models.F('start_of_disease')),
                                   name='ck_end_after_start_disease'),
        ]