from .base_repository import BaseRepository
from repository.models.disease import Disease


class DiseaseRepository(BaseRepository):
    def __init__(self):
        super().__init__(model = Disease)