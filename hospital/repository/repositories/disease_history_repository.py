from .base_repository import BaseRepository
from ..models import DiseaseHistory


class DiseaseHistoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=DiseaseHistory)
