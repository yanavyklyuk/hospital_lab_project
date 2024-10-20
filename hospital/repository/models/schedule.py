from django.db import models


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
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)


def __str__(self):
    return f"Schedule: {self.doctor} - {self.day} - {self.start_time} - {self.end_time}"
