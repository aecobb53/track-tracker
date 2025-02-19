from datetime import datetime, timezone
import json
from typing import List, Dict, Any
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from pydantic import BaseModel, model_validator
from enum import Enum
from uuid import uuid4

from .event import EventParser


class AthleteData(BaseModel):
    uid: str
    update_datetime: datetime

    first_name: str | None = None
    last_name: str | None = None
    team: str | None = None
    gender: str | None = None
    graduation_year: int | None = None

    # @model_validator(mode='before')
    # def validate_fields(cls, fields):

    @property
    def put(self):
        output = self.model_dump()
        if output.get('graduation_year') is not None:
            year = output['graduation_year'] - datetime.now(timezone.utc).year
            if year < 0:
                output['current_year'] = f'Graduated'
            elif year == 0:
                output['current_year'] = f'Senior'
            elif year == 1:
                output['current_year'] = f'Junior'
            elif year == 2:
                output['current_year'] = f'Sophomore'
            elif year == 3:
                output['current_year'] = f'Freshman'
            elif year > 3:
                output['current_year'] = f'Not in HS yet'
        return output

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class AthleteApiCreate(BaseModel):
    first_name: str
    last_name: str
    graduation_year: int | None = None
    team: str
    gender: str | None = None

    def cast_data_object(self) -> AthleteData:
        """Return a data object based on the AthleteData class"""
        content = self.model_dump()
        content['uid'] = str(uuid4())
        content['update_datetime'] = datetime.now(timezone.utc)
        data_obj = AthleteData(**content)
        return data_obj


class AthleteDBBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    uid: str = Field(unique=True)
    update_datetime: datetime | None = None

    first_name: str | None = None
    last_name: str | None = None
    team: str | None = None
    gender: str | None = None
    graduation_year: int | None = None

    # active: bool = True

    def cast_data_object(self) -> AthleteData:
        """Return a data object based on the AthleteData class"""
        content = self.model_dump()
        data_obj = AthleteData(**content)
        return data_obj


class AthleteDBCreate(AthleteDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        return fields



class AthleteDBRead(AthleteDBBase):
    pass


class AthleteDB(AthleteDBBase, table=True):
    __tablename__ = "athlete"


class AthleteFilter(BaseModel):
    uid: List[str] | None = None

    first_name: List[str] | None = None
    last_name: List[str] | None = None
    team: List[str] | None = None
    gender: List[str] | None = None
    graduation_year: List[int] | None = None

    limit: int = 1000
    order_by: List[str] = ['last_name', 'first_name']
    offset: int = 0

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # if isinstance(fields.get('active'), list):
        #     fields['active'] = fields['active'][0]
        if isinstance(fields.get('limit'), list):
            fields['limit'] = fields['limit'][0]
        if isinstance(fields.get('offset'), list):
            fields['offset'] = fields['offset'][0]
        return fields

    def apply_filters(self, database_object_class: AthleteDBBase, query: select) -> select:
        """Apply the filters to the query"""
        if self.uid:
            query = query.filter(database_object_class.uid.in_(self.uid))

        if self.first_name:
            query = query.filter(database_object_class.first_name.in_(self.first_name))
        if self.last_name:
            query = query.filter(database_object_class.last_name.in_(self.last_name))
        if self.team:
            query = query.filter(database_object_class.team.in_(self.team))
        if self.gender:
            query = query.filter(database_object_class.gender.in_(self.gender))
        if self.graduation_year:
            query = query.filter(database_object_class.graduation_year.in_(self.graduation_year))

        if self.limit:
            query = query.limit(self.limit)
        for order_by in self.order_by:
            query = query.order_by(getattr(database_object_class, order_by))
        if self.offset:
            query = query.offset(self.offset)

        return query
