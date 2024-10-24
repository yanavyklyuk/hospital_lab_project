from django.db import models
from .doctor import Doctor
from django.core.exceptions import ValidationError
from django.db.models import Q


class Schedule(models.Model):
    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    minutes_per_patient = models.IntegerField()
    cabinet_number = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Schedule: {self.doctor} - {self.day} - {self.start_time} - {self.end_time}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be greater than start time.")

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'
        ordering = ['day', 'start_time']
        constraints = [
            models.UniqueConstraint(fields=['day', 'start_time', 'end_time', 'cabinet_number'], name='unique_schedule'),
            models.CheckConstraint(check=Q(end_time__gt=models.F('start_time')),
                                   name='ck_end_after_start_time'),
            models.CheckConstraint(check=Q(minutes_per_patient__gt=0), name='ck_minutes_per_patient'),
            models.CheckConstraint(check=Q(cabinet_number__gt=0), name='ck_cabinet_number'),
        ]