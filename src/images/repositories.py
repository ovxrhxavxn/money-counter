from database.repositories import SQLAlchemyRepository
from database.orm.sqlalchemy.models import Image


class ImageRepository(SQLAlchemyRepository[Image]):

    def __init__(self):
        super().__init__(Image)