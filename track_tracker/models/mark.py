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

    athlete: AthleteData | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields['wind'] is None:
            fields['wind'] = 0.0
        fields['athlete'] = None
        mark = Mark.parse_event_mark(event=fields['event'], mark=fields['mark'])
        fields['mark'] = mark
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
# #     name: List[str] | None = None
# #     venue: List[str] | None = None
# #     # geometry: List[Point | Polygon] | None = None
# #     geometry: PointModel | PolygonModel | MultiPolygonModel | None = None
# #     active: bool | str | None = True
# #     # closures_start: datetime
# #     # closures_end: datetime
# #     # event_start: datetime
# #     # event_end: datetime
# #     event_after: datetime | None = None
# #     event_before: datetime | None = None

# #     expected_impact: List[ExpectedImpact] | None = None
# #     source: List[str] | None = None

# #     creation_datetime_after: datetime | None = None
# #     creation_datetime_before: datetime | None = None
# #     limit: int = 1000
# #     order_by: List[str] = ['creation_datetime']
# #     offset: int = 0

# #     @model_validator(mode='before')
# #     def validate_fields(cls, fields):
# #         if isinstance(fields.get('event_after'), list):
# #             fields['event_after'] = fields['event_after'][0]
# #         if isinstance(fields.get('event_before'), list):
# #             fields['event_before'] = fields['event_before'][0]

# #         if isinstance(fields.get('creation_datetime_after'), list):
# #             fields['creation_datetime_after'] = fields['creation_datetime_after'][0]
# #         if isinstance(fields.get('creation_datetime_before'), list):
# #             fields['creation_datetime_before'] = fields['creation_datetime_before'][0]
# #         if isinstance(fields.get('active'), list):
# #             fields['active'] = fields['active'][0]
# #         if isinstance(fields.get('geometry'), list):
# #             geometry = fields['geometry'][0]
# #             geometry = shapely.wkt.loads(geometry)
# #             geometry = PolygonModel(**json.loads(to_geojson(geometry)))
# #             fields['geometry'] = geometry
# #         if isinstance(fields.get('limit'), list):
# #             fields['limit'] = fields['limit'][0]
# #         if isinstance(fields.get('offset'), list):
# #             fields['offset'] = fields['offset'][0]
# #         return fields

# #     def apply_filters(self, database_object_class: MarkDBBase, query: select) -> select:
# #         """Apply the filters to the query"""
# #         if self.uid:
# #             query = query.filter(database_object_class.uid.in_(self.uid))
# #         if self.name:
# #             query = query.filter(database_object_class.name.in_(self.name))
# #         if self.active is not None:
# #             if not isinstance(self.active, str):
# #                 query = query.filter(database_object_class.active == self.active)
# #         if self.venue:
# #             query = query.filter(database_object_class.venue.in_(self.venue))
# #         if self.source:
# #             query = query.filter(database_object_class.source.in_(self.source))
# #         if self.geometry:
# #             geometry = from_geojson(self.geometry.model_dump_json())
# #             query = query.filter(
# #                 func.ST_Intersects(database_object_class.geometry, from_shape(geometry))
# #             )

# #         if self.event_after:
# #             query = query.filter(database_object_class.event_start >= self.event_after)
# #         if self.event_before:
# #             query = query.filter(database_object_class.event_end <= self.event_before)

# #         if self.creation_datetime_after:
# #             query = query.filter(database_object_class.creation_datetime >= self.creation_datetime_after)
# #         if self.creation_datetime_before:
# #             query = query.filter(database_object_class.creation_datetime <= self.creation_datetime_before)
# #         if self.limit:
# #             query = query.limit(self.limit)
# #         for order_by in self.order_by:
# #             query = query.order_by(getattr(database_object_class, order_by))
# #         if self.offset:
# #             query = query.offset(self.offset)

# #         return query


