from django.db import models


class Specialisation(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Specialisation'
        verbose_name_plural = 'Specialisations'
        ordering = ['name']