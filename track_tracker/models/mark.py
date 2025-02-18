from datetime import datetime, timezone
import json
from typing import List, Dict, Any
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from pydantic import BaseModel, model_validator
from enum import Enum
from uuid import uuid4

from .athlete import AthleteData
from .event import EventParser


class Mark(BaseModel):
    event_str: str
    mark_str: str
    minutes: int | None = None
    seconds: int | None = None
    subsecond: float | None = None
    feet: int | None = None
    inches: float | None = None

    @classmethod
    def parse_event_mark(cls, event: str, mark: str):
        minutes, seconds, subsecond, feet, inches = EventParser.parse_event_mark(event_s=event, mark_s=mark)
        obj = cls(
            event_str=event,
            mark_str=mark,
            minutes=minutes,
            seconds=seconds,
            subsecond=subsecond,
            feet=feet,
            inches=inches,
        )
        return obj

    @property
    def format(self):
        if self.minutes is not None:
            minutes = str(self.minutes)
        if self.seconds is not None:
            seconds = str(self.seconds).rjust(2, '0')
        if self.subsecond is not None:
            subsecond = str(self.subsecond).rjust(2, '0')
        if self.feet is not None:
            feet = str(self.feet).rjust(2, '0')
        if self.inches is not None:
            inches = str(self.inches * 12 / 100).rjust(2, '0')
        if all([minutes, seconds, subsecond]):
            return f"{minutes}:{seconds}.{subsecond}"
        elif all([seconds, subsecond]):
            return f"{seconds}.{subsecond}"
        elif all([feet, inches]):
            return f"{feet}.{inches}"

    @property
    def put(self):
        output = f"{self.event_str}::{self.mark_str}"

    @classmethod
    def build(cls, input):
        event, mark = input.split('::')
        return cls.parse_event_mark(event=event, mark=mark)


class MarkData(BaseModel):
    uid: str
    update_datetime: datetime

    event: str
    heat: int
    place: int
    wind: float
    attempt: int | None = None
    athlete: AthleteData | None = None
    team: str | None = None
    meet_date: datetime
    mark: Mark
    meet: str
    gender: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        x=1
        return fields

    @property
    def put(self):
        output = self.model_dump()
        return output


class MarkApiCreate(BaseModel):
    event: str
    heat: int
    place: int
    wind: float | None = None
    attempt: int | None = None
    athlete_uid: str | None = None
    athlete_first_name: str | None = None
    athlete_last_name: str | None = None
    team: str | None = None
    meet_date: datetime
    mark: Mark
    meet: str
    gender: str | None = None

    athlete: AthleteData | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields['wind'] is None:
            fields['wind'] = 0.0
        fields['athlete'] = None
        mark = Mark.parse_event_mark(event=fields['event'], mark=fields['mark'])
        fields['mark'] = mark
        fields['gender'] = EventParser.parse_event_gender(event_s=fields['event'])
        return fields

    def cast_data_object(self) -> MarkData:
        """Return a data object based on the MarkData class"""
        content = self.model_dump()
        content['uid'] = str(uuid4())
        content['update_datetime'] = datetime.now(timezone.utc)
        data_obj = MarkData(**content)
        return data_obj

    @property
    def put(self):
        output = self.model_dump()
        return output


class MarkDBBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    uid: str = Field(unique=True)
    update_datetime: datetime | None = None

    event: str
    heat: int
    place: int
    wind: float
    attempt: int | None = None
    athlete_uid: str = Field(foreign_key="athlete.uid")
    team: str | None = None
    meet_date: datetime
    mark: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
    meet: str
    gender: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        return fields

    def cast_data_object(self) -> MarkData:
        """Return a data object based on the MarkData class"""
        content = self.model_dump()
        data_obj = MarkData(**content)
        return data_obj


class MarkDBCreate(MarkDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        print(f"IN DB CREATE VALIDATE")
        if not isinstance(fields, dict):
            fields = fields.model_dump()
        print(fields)
        fields['athlete_uid'] = fields['athlete']['uid']
        # fields['mark'] = ['fields']['mark']['put']
        print('---')
        print(fields)
        print(f"DB CREATE VALIDATE")
        return fields


class MarkDBRead(MarkDBBase):
    pass


class MarkDB(MarkDBBase, table=True):
    __tablename__ = "mark"


class MarkFilter(BaseModel):
    uid: List[str] | None = None

    event: List[str] = []

    # heat: List[int] = []
    # place: List[int] = []
    # wind: List[float] = []
    # attempt: List[int] = []

    athlete_uid: List[str] = []
    team: List[str] = []
    meet: List[str] = []
    gender: List[str] = []

    # meet_date: List[datetime] = []
    # mark: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))

    limit: int = 1000
    order_by: List[str] = ['event', 'place']
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

    def apply_filters(self, database_object_class: MarkDBBase, query: select) -> select:
        """Apply the filters to the query"""
        if self.uid:
            query = query.filter(database_object_class.uid.in_(self.uid))

        if self.event:
            query = query.filter(database_object_class.event.in_(self.event))
        # heat: List[int] = []
        # place: List[int] = []
        # wind: List[float] = []

        # attempt: List[int] = []
        if self.athlete_uid:
            query = query.filter(database_object_class.athlete_uid.in_(self.athlete_uid))
        if self.team:
            query = query.filter(database_object_class.team.in_(self.team))
        if self.meet:
            query = query.filter(database_object_class.meet.in_(self.meet))
        # meet_date: List[datetime] = []

        if self.limit:
            query = query.limit(self.limit)
        for order_by in self.order_by:
            query = query.order_by(getattr(database_object_class, order_by))
        if self.offset:
            query = query.offset(self.offset)

        return query


