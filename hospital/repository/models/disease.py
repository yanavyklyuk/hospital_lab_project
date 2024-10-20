from django.db import models


class Disease(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__ (self):
        return f"Disease: {self.name}"

    class Meta:
        verbose_name = "Disease"
        verbose_name_plural = "Diseases"
        ordering = ['name']