import datetime

from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload

from api.exceptions import InvalidRequestException
from database import models, schemas


def find_system_item_by_id(id, db):
    return db.query(models.SystemItem).filter(models.SystemItem.id == id)


def find_updates_units_by_item_id(id, db):
    return db.query(models.SystemItemHistoryUnit).filter(
        models.SystemItemHistoryUnit.item_id == id)


def get_all_categories(db):
    return db.query(models.SystemItem).filter(
        models.SystemItem.type == schemas.SystemItemType['FOLDER']).all()


def create_system_item(id, url, type, size, parent_id, date):
    return models.SystemItem(
        id=id,
        url=url,
        type=type,
        size=size,
        parentId=parent_id,
        date=date,
    )


def create_updates_item(item, parent_id, date):
    return models.SystemItemHistoryUnit(
        item_id=item.id,
        url=item.url,
        type=schemas.SystemItemType(item.type),
        size=item.size,
        parent_id=parent_id,
        item_parent_id=item.parentId,
        date=date)


def imports(item, update_date, db):
    ids = set(db.scalars(select(models.SystemItem.id)).all())

    if item.parentId and item.parentId not in ids:
        raise InvalidRequestException(f"Элемента {item.parentId} не найдено")

    parent_item = find_system_item_by_id(item.parentId, db).first()

    if parent_item and parent_item.type != schemas.SystemItemType['FOLDER']:
        raise InvalidRequestException(
            f"Элемент {item.parentId} не является FOLDER")

    old_item = db.query(models.SystemItem).filter(
        models.SystemItem.id == item.id)

    if old_item.first():
        old_item.update(item.dict())
        old_item.first().date = update_date

    else:
        system_item = create_system_item(
            id=item.id,
            url=item.url,
            type=schemas.SystemItemType(item.type),
            size=item.size,
            parent_id=item.parentId,
            date=update_date,
        )
        db.add(system_item)

    db.commit()


def delete(id, db):
    item = find_system_item_by_id(id, db).first()
    updates_items = find_updates_units_by_item_id(id, db)

    if item:
        for i in updates_items.all():
            db.delete(i)

        db.delete(item)
        db.commit()
        return item


def nodes(id, db):
    return find_system_item_by_id(id, db).options(
        joinedload(models.SystemItem.children)).first()


def updates(date, db):
    return db.query(models.SystemItemHistoryUnit).filter(
        and_(
            models.SystemItemHistoryUnit.date.between(
                date - datetime.timedelta(hours=24),
                date
            ),
            models.SystemItemHistoryUnit.type == schemas.SystemItemType['FILE']
        )
    ).order_by(models.SystemItemHistoryUnit.date).all()


def history(id, dateStart, dateEnd, db):
    return db.query(models.SystemItemHistoryUnit).filter(and_(
        models.SystemItemHistoryUnit.date.between(dateStart, dateEnd),
        models.SystemItemHistoryUnit.item_id == id)).order_by(
        models.SystemItemHistoryUnit.date).all()
