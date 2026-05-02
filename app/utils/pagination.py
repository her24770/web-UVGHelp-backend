from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc


# aplica búsqueda, ordenamiento y paginación a cualquier modelo, retorna dict con items y metadata
def paginate(
    db: Session,
    model,
    page: int,
    limit: int,
    q: str | None,
    sort: str | None,
    order: str,
    search_field: str = "nombre",
) -> dict:
    query = select(model)

    # filtra por campo de texto si se envió ?q=
    if q:
        col = getattr(model, search_field, None)
        if col is not None:
            query = query.where(col.ilike(f"%{q}%"))

    # ordena por el campo indicado si existe en el modelo
    if sort:
        col = getattr(model, sort, None)
        if col is not None:
            query = query.order_by(desc(col) if order == "desc" else asc(col))

    # cuenta el total con los filtros ya aplicados
    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0

    # aplica offset y limit para la página solicitada
    items = list(db.execute(query.offset((page - 1) * limit).limit(limit)).scalars().all())

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": max(1, -(-total // limit)),
    }
