from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int = 50
    offset: int = 0


def get_pagination(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> Pagination:
    return Pagination(limit=limit, offset=offset)