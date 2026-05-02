from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


# esquema genérico de respuesta paginada, aplica para cualquier entidad
class PagedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    limit: int
    pages: int
