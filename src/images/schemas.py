from typing import TypeAlias, Annotated

from pydantic import BaseModel


path: TypeAlias = str


class ImageSchema(BaseModel):

    path: Annotated[path, 'A correct path to an image']


class ImageFromDB(ImageSchema):

    id: int