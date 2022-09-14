from datetime import datetime

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from api import services
from api.exceptions import NotFoundException
from database import schemas
from database.db import get_db

router = APIRouter()


@router.post(
    '/imports',
    status_code=status.HTTP_200_OK,
)
async def imports(
        request: schemas.SystemItemImportRequest = Body(),
        db: Session = Depends(get_db)
):
    """
    Импортирует элементы файловой системы. Элементы импортированные повторно
    обновляют текущие. Изменение типа элемента с папки на файл и с файла на
    папку не допускается. Порядок элементов в запросе является произвольным.
    """
    services.imports(request.items, request.updateDate, db)

    return status.HTTP_200_OK


@router.delete(
    '/delete/{id}',
    status_code=status.HTTP_200_OK,
)
async def delete(id: str, db: Session = Depends(get_db)):
    """
    Удалить элемент по идентификатору. При удалении категории удаляются все
    дочерние элементы. Доступ к статистике (истории обновлений) удаленного
    элемента невозможен.
    """
    item = services.delete(id, db)

    if not item:
        raise NotFoundException(f"Элемента с id: {id} не найдено")

    return status.HTTP_200_OK


@router.get(
    '/nodes/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SystemItem,
)
async def nodes(id: str, db: Session = Depends(get_db)):
    """
    Получить информацию об элементе по идентификатору.
    При получении информации о папке также предоставляется
    информация о её дочерних элементах.
    """
    item = services.nodes(id, db)

    if not item:
        raise NotFoundException(f"Элемента с id: {id} не найдено")
    return item


@router.get(
    '/updates',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SystemItemHistoryUnitResponse,
)
async def updates(date: datetime, db: Session = Depends(get_db)):
    """
    Получение списка файлов, которые были обновлены за последние 24 часа
    включительно [date - 24h, date] от времени переданном в запросе.
    """
    return services.updates(date, db)


@router.get(
    '/node/{id}/history',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SystemItemHistoryUnitResponse,
)
async def history(
        id: str,
        dateStart: datetime,
        dateEnd: datetime,
        db: Session = Depends(get_db)
):
    """
    Получение истории обновлений по элементу за заданный
    полуинтервал [from, to). История по удаленным элементам недоступна.
    """
    return services.history(id, dateStart, dateEnd, db)
