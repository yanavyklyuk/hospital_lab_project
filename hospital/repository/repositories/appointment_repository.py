from .base_repository import BaseRepository
from repository.models.appointment import Appointment


class AppointmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(model = Appointment)