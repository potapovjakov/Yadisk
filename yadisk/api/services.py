from collections import deque

from api import repository
from api.exceptions import InvalidRequestException
from database import schemas


def update_unit_size(id, dt, db):
    item = repository.find_system_item_by_id(id, db).first()
    if not item:
        return
    parent = repository.find_system_item_by_id(item.parentId, db).first()

    if item.type == schemas.SystemItemType['FOLDER']:
        queue = deque()
        size_sum, size_count = 0, 0
        queue.append(item)
        while queue:
            current = queue.popleft()

            for child in current.children:
                if child.type == schemas.SystemItemType['FILE']:
                    size_sum += child.size
                    size_count += 1
                else:
                    queue.append(child)
        if size_count != 0:
            item.size = size_sum
            item.date = dt
            add_updates_unit(item, dt, db)
    db.commit()

    if not parent:
        return
    update_unit_size(parent.id, dt, db)


def imports(items, datetime, db):
    exist_id = set(i.id for i in repository.get_all_categories(db))
    new_id = set(
        i.id for i in items if i.type == schemas.SystemItemType['FOLDER']
    )
    items_without_new_parent_id = []
    items_with_new_parent_id = []

    for item in items:
        if not item.parentId or item.parentId in exist_id:
            items_without_new_parent_id.append(item)
        elif item.parentId in new_id:
            items_with_new_parent_id.append(item)
        else:
            raise InvalidRequestException('Родитель должен быть FOLDER')

    for item in items_without_new_parent_id:
        _import(item, datetime, db)
        update_unit_size(item.id, datetime, db)

    for item in items_with_new_parent_id:
        new_item = item.copy()
        new_item.parentId = None
        _import(new_item, datetime, db)

    for item in items_with_new_parent_id:
        new_item = repository.find_system_item_by_id(item.id, db)
        new_item.update(item.dict())
        db.commit()
        update_unit_size(item.id, datetime, db)

    for i in items:
        add_updates_unit(i, datetime, db)


def add_updates_unit(item, updates_date, db):
    parent_updates_unit = repository.find_updates_units_by_item_id(
        item.parentId,
        db,
    ).first()
    parent_id = None
    if parent_updates_unit:
        parent_id = parent_updates_unit.id
    updates_unit = repository.create_updates_item(
        item,
        parent_id,
        updates_date,
    )
    db.add(updates_unit)
    db.commit()


def _import(item, update_date, db):
    repository.imports(item, update_date, db)


def delete(id, db):
    return repository.delete(id, db)


def nodes(id, db):
    return repository.nodes(id, db)


def updates(date, db):
    return schemas.SystemItemHistoryUnitResponse(
        items=[u.__dict__ for u in repository.updates(date, db)])


def history(id, dateStart, dateEnd, db):
    return schemas.SystemItemHistoryUnitResponse(
        items=[u.__dict__ for u in
               repository.history(id, dateStart, dateEnd, db)])
