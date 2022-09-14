from uuid import uuid4

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP
from sqlalchemy.orm import relationship

from database.db import Base
from database.schemas import SystemItemType


class SystemItem(Base):
    __tablename__ = 'system_items'

    id = Column(
        String,
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    url = Column(String, nullable=True)
    type = Column(ENUM(SystemItemType))
    parentId = Column(
        String,
        ForeignKey('system_items.id'),
        nullable=True,
    )
    size = Column(Integer, default=0, nullable=True)
    date = Column(TIMESTAMP(timezone=False), nullable=False)
    children = relationship(
        'SystemItem',
        cascade="all, delete",
        lazy='joined'
    )


class SystemItemHistoryUnit(Base):
    __tablename__ = 'system_history'

    id = Column(
        String,
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    item_id = Column(String, default=uuid4, nullable=False)
    url = Column(String, nullable=True)
    type = Column(ENUM(SystemItemType))
    item_parent_id = Column(String, nullable=True)
    parent_id = Column(
        String,
        ForeignKey('system_history.id'),
        nullable=True
    )
    size = Column(Integer, default=0, nullable=True)
    date = Column(TIMESTAMP(timezone=False), nullable=False)
    children = relationship(
        'SystemItemHistoryUnit',
        cascade="all, delete"
    )
