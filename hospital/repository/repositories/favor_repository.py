from .base_repository import BaseRepository
from ..models.favor import Favor


class FavorRepository(BaseRepository):
    def __init__(self):
        super().__init__(model = Favor)