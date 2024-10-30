from .base_repository import BaseRepository
from ..models import DiseaseHistory


class DiseaseHistoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=DiseaseHistory)

    def get_by_patient(self, patient_id):
        diseases = self.model.objects.filter(patient=patient_id)
        if not diseases.exists():
            return None
        return diseases
