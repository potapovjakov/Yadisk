from datetime import datetime
from enum import Enum, unique
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, root_validator, validator

from api.exceptions import InvalidRequestException
from api.utils import convert_datetime


@unique
class SystemItemType(str, Enum):
    FILE = 'FILE'
    FOLDER = 'FOLDER'


class SystemItem(BaseModel):
    id: str
    url: Optional[str] = None
    date: datetime
    parentId: Optional[str] = None
    type: SystemItemType
    size: Optional[int] = None
    children: Optional[List['SystemItem']] = None

    @validator('children')
    def empty_list_to_none(cls, value):
        if not value:
            return None
        return value

    class Config:
        orm_mode = True

        json_encoders = {
            datetime: lambda dt: convert_datetime(dt)
        }


class SystemItemImport(BaseModel):
    id: str
    url: Optional[str] = None
    parentId: Optional[str] = None
    type: SystemItemType
    size: Optional[int] = None

    @root_validator
    def item_check(cls, value):
        if value['type'] == SystemItemType['FOLDER']:
            if value.get('size') is None:
                pass
            else:
                if value.get('size') != 0:
                    raise InvalidRequestException(
                        'Размер папки при импорте должен быть null'
                    )
            if value.get('url') is None:
                pass
            else:
                raise InvalidRequestException(
                    'URL папки при импорте должен быть null'
                )

        if value['type'] == SystemItemType['FILE'] and value.get('size', -1) <= 0:
            raise InvalidRequestException(
                'Размер файла при иморте должен быть больше 0')
        if value['type'] == SystemItemType['FILE'] and len(value.get('url')) > 255:
            raise InvalidRequestException(
                'Длина URL файла не может быть более 255 символов'
            )
        return value


class SystemItemImportRequest(BaseModel):
    items: List[SystemItemImport] = []
    updateDate: datetime

    @validator('items')
    def must_not_contain_same_ids(cls, value):
        request_ids_set = set(item.id for item in value)
        if len(request_ids_set) != len(value):
            raise InvalidRequestException(
                'ID всех элементов должны быть уникальными ')
        return value


class SystemItemHistoryUnit(BaseModel):
    id: str
    url: Optional[str] = None
    parentId: Optional[str]
    type: SystemItemType
    size: Optional[int] = None
    date: datetime


class SystemItemHistoryUnitResponse(BaseModel):
    items: List[SystemItemHistoryUnit] = []

