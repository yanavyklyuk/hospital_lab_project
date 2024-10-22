from .base_repository import BaseRepository
from ..models.patient import Patient


class PatientRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Patient)
