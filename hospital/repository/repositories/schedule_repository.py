from .base_repository import BaseRepository
from ..models.schedule import Schedule


class ScheduleRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=Schedule)
