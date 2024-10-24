from django.db import models
from django.db.models import Q


class Favor(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}: {self.cost} UAH"

    class Meta:
        verbose_name = "Favor"
        verbose_name_plural = "Favors"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'cost'], name='uq_name_cost'),
            models.CheckConstraint(check = Q(cost__gte=0), name='ck_favor_cost'),
        ]