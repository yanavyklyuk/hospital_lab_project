from .base_repository import BaseRepository
from ..models.specialisation import Specialisation


class SpecialisationRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Specialisation)
