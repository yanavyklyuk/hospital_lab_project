from .base_repository import BaseRepository
from ..models.schedule import Schedule


class ScheduleRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Schedule)

    def get_schedule_for_doctor(self, doctor_id):
        schedules = self.model.objects.filter(doctor_id=doctor_id)
        if not schedules.exists():
            return None
        return schedules