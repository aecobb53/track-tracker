from datetime import datetime, timezone
import json
import re
from typing import List, Dict, Any
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from sqlmodel import or_, and_
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
    inches: int | None = None
    fractions: float | None = None

    @classmethod
    def parse_event_mark(cls, event: str, mark: str):
        minutes, seconds, subsecond, feet, inches, fractions = EventParser.parse_event_mark(event_s=event, mark_s=mark)
        obj = cls(
            event_str=event,
            mark_str=mark,
            minutes=minutes,
            seconds=seconds,
            subsecond=subsecond,
            feet=feet,
            inches=inches,
            fractions=fractions,
        )
        return obj

    @property
    def format(self):
        minutes = str(self.minutes) if self.minutes is not None else None
        seconds = str(self.seconds) if self.seconds is not None else None
        subsecond = str(self.subsecond) if self.subsecond is not None else None

        feet = str(self.feet) if self.feet is not None else None
        inches = str(self.inches) if self.inches is not None else None
        fractions = str(self.fractions) if self.fractions is not None else None

        if all([minutes, seconds, subsecond]):
            return f"{minutes}:{seconds.zfill(2)}.{subsecond[2:]}"
        elif all([seconds, subsecond]):
            return f"{seconds}.{subsecond[2:]}"
        elif all([feet, inches, fractions]):
            return f"{feet}-{inches.zfill(2)}.{fractions[2:]}"
        elif all([feet, inches]):
            return f"{feet}-{inches}"

    @property
    def put(self):
        output = f"{self.event_str}::{self.mark_str}"
        return output

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

    @property
    def rest_output(self):
        output = self.model_dump_json()
        return output


class MarkApiCreate(BaseModel):
    event: str
    heat: int
    place: int
    wind: float | None = None
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
        if not fields.get('wind'):
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
        if not isinstance(fields, dict):
            fields = fields.model_dump()
        fields['athlete_uid'] = fields['athlete']['uid']
        # fields['mark'] = ['fields']['mark']['put']
        return fields


class MarkDBRead(MarkDBBase):
    pass


class MarkDB(MarkDBBase, table=True):
    __tablename__ = "mark"


class MarkFilter(BaseModel):
    uid: List[str] | None = None

    event: List[str] = []

    heat: List[str] = []
    place: List[str] = []
    wind: List[str] = []

    athlete_uid: List[str] = []
    team: List[str] = []
    first_name: List[str] = []
    last_name: List[str] = []
    meet: List[str] = []
    gender: List[str] = []

    meet_date: List[str] = []
    # mark: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))

    limit: int = 1000
    order_by: List[str] = ['event', 'place']
    offset: int = 0


    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields.get('event'):
            event = []
            [event.extend(i.split(',')) for i in fields['event']]
            fields['event'] = [e.strip() for e in event]

        if fields.get('heat'):
            heat = []
            for i in fields['heat']:
                i_l = i.split(',')
                for ii in i_l:
                    ii = ii.strip()
                    if ii:
                        heat.append(ii)
            fields['heat'] = heat

        if fields.get('place'):
            place = []
            for i in fields['place']:
                i_l = i.split(',')
                for ii in i_l:
                    ii = ii.strip()
                    if ii:
                        place.append(ii)
            fields['place'] = place

        if fields.get('wind'):
            wind = []
            for i in fields['wind']:
                i_l = i.split(',')
                for ii in i_l:
                    ii = ii.strip()
                    if ii:
                        wind.append(ii)
            fields['wind'] = wind

        if fields.get('team'):
            team = []
            [team.extend(i.split(',')) for i in fields['team']]
            fields['team'] = [t.strip() for t in team]

        if fields.get('meet'):
            meet = []
            [meet.extend(i.split(',')) for i in fields['meet']]
            fields['meet'] = [m.strip() for m in meet]

        if fields.get('first_name'):
            first_name = []
            [first_name.extend(i.split(',')) for i in fields['first_name']]
            fields['first_name'] = [f.strip() for f in first_name]

        if fields.get('last_name'):
            last_name = []
            [last_name.extend(i.split(',')) for i in fields['last_name']]
            fields['last_name'] = [l.strip() for l in last_name]

        if fields.get('athlete_uid'):
            athlete_uid = []
            [athlete_uid.extend(i.split(',')) for i in fields['athlete_uid']]
            fields['athlete_uid'] = [g.strip() for g in athlete_uid]

        if fields.get('gender'):
            gender = []
            [gender.extend(i.split(',')) for i in fields['gender']]
            fields['gender'] = [g.strip() for g in gender]

        if fields.get('meet_date'):
            meet_date = []
            [meet_date.extend(i.split(',')) for i in fields['meet_date']]
            fields['meet_date'] = [m.strip() for m in meet_date]

        # if isinstance(fields.get('active'), list):
        #     fields['active'] = fields['active'][0]
        if isinstance(fields.get('limit'), list):
            fields['limit'] = fields['limit'][0]
        if isinstance(fields.get('offset'), list):
            fields['offset'] = fields['offset'][0]
        return fields

    def apply_filters(self, database_object_class: MarkDBBase, query: select) -> select:
        """Apply the filters to the query"""
        def apply_modifier(query, db_obj_cls, string):
            if string.startswith('='):
                return query.filter(db_obj_cls == string[1:])
            elif string.startswith('>='):
                return query.filter(db_obj_cls >= string[2:])
            elif string.startswith('>'):
                return query.filter(db_obj_cls > string[1:])
            elif string.startswith('<='):
                return query.filter(db_obj_cls <= string[2:])
            elif string.startswith('<'):
                return query.filter(db_obj_cls < string[1:])
            elif string.startswith('!='):
                return query.filter(db_obj_cls != string[2:])

        if self.uid:
            query = query.filter(database_object_class.uid.in_(self.uid))

        if self.event:
            filter_list = [database_object_class.event.contains(e) for e in self.event]
            query = query.filter(or_(*filter_list))

        if self.heat:
            filter_list = []
            for heat in self.heat:
                query = apply_modifier(query, database_object_class.heat, heat)

        if self.place:
            filter_list = []
            for place in self.place:
                query = apply_modifier(query, database_object_class.place, place)

        if self.wind:
            filter_list = []
            for wind in self.wind:
                query = apply_modifier(query, database_object_class.wind, wind)

        if self.athlete_uid:
            query = query.filter(database_object_class.athlete_uid.in_(self.athlete_uid))

        if self.team:
            filter_list = [database_object_class.team.contains(t) for t in self.team]
            query = query.filter(or_(*filter_list))

        if self.meet:
            filter_list = [database_object_class.meet.contains(m) for m in self.meet]
            query = query.filter(or_(*filter_list))

        if self.team:
            filter_list = [database_object_class.team.contains(t) for t in self.team]
            query = query.filter(or_(*filter_list))

        if self.first_name:
            filter_list = [database_object_class.first_name.contains(f) for f in self.first_name]
            query = query.filter(or_(*filter_list))

        if self.last_name:
            filter_list = [database_object_class.last_name.contains(l) for l in self.last_name]
            query = query.filter(or_(*filter_list))

        if self.athlete_uid:
            filter_list = [database_object_class.athlete_uid.contains(a) for a in self.athlete_uid]
            query = query.filter(or_(*filter_list))

        if self.gender:
            filter_list = [database_object_class.gender.contains(g) for g in self.gender]
            query = query.filter(or_(*filter_list))

        if self.meet_date:
            for meet_date in self.meet_date:
                if meet_date.startswith('='):
                    query = query.filter(database_object_class.meet_date == datetime.strptime(meet_date[1:], "%Y-%m-%d"))
                elif meet_date.startswith('>='):
                    query = query.filter(database_object_class.meet_date >= datetime.strptime(meet_date[2:], "%Y-%m-%d"))
                elif meet_date.startswith('<='):
                    query = query.filter(database_object_class.meet_date <= datetime.strptime(meet_date[2:], "%Y-%m-%d"))

        if self.limit:
            query = query.limit(self.limit)
        for order_by in self.order_by:
            query = query.order_by(getattr(database_object_class, order_by))
        if self.offset:
            query = query.offset(self.offset)

        return query
