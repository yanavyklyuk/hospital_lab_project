from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from abc import ABC, abstractmethod
from typing import Type


class BaseRepository(ABC):
    def __init__(self, model: Type[models.Model]):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, id):
        try:
            return self.model.objects.get(pk = id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        if instance is None:
            raise ObjectDoesNotExist("Instance does not exist.")

        if not isinstance(instance, self.model):
            raise ValueError("Provided instance is not of the correct model type.")

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
            else:
                raise ValueError(f"Invalid field: {key}")

        instance.save()
        return instance

    def delete(self, instance):
        if instance is None:
            raise ObjectDoesNotExist("Instance does not exist.")

        if not isinstance(instance, self.model):
            raise ValueError("Provided instance is not of the correct model type.")

        instance.delete()