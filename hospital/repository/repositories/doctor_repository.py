from .base_repository import BaseRepository
from repository.models.doctor import Doctor


class DoctorRepository(BaseRepository):
    def __init__(self):
        super().__init__(model = Doctor)