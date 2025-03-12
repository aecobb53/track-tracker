from datetime import datetime, timezone, timedelta
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
from .common import apply_modifier


class Result(BaseModel):
    event_str: str
    result_str: str
    minutes: int | None = None
    seconds: int | None = None
    subsecond: float | None = None
    feet: int | None = None
    inches: int | None = None
    fractions: float | None = None

    @classmethod
    def parse_event_result(cls, event: str, result: str):
        minutes, seconds, subsecond, feet, inches, fractions = EventParser.parse_event_result(event_s=event, result_s=result)
        obj = cls(
            event_str=event,
            result_str=result,
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
    def format_smaller_value(self):
        """
        Force results in terms of seconds or inches
        """
        """
        tmp = timedelta(
            minutes=minutes or 0,
            seconds=seconds or 0,
            milliseconds=subsecond or 0,
        )
        tmp_min = tmp.seconds // 60
        tmp_sec = tmp.seconds % 60
        tmp_microseconds = tmp.microseconds
        tmp_format = f"{tmp_min}:{tmp_sec}.{tmp_microseconds}"
        print(f"tmp: {tmp}, tmp_min: {tmp_min}, tmp_sec: {tmp_sec}, tmp_microseconds: {tmp_microseconds}, tmp_format: {tmp_format}")

        """
        if self.minutes or self.seconds or self.subsecond:
            minutes = self.minutes or 0
            seconds = self.seconds or 0
            subsecond = self.subsecond or 0
            seconds += subsecond
            value = timedelta(minutes=minutes, seconds=seconds)
            formatted = float(value.total_seconds())
            return formatted
        elif self.feet or self.inches or self.fractions:
            feet = self.feet or 0
            inches = self.inches or 0
            fractions = self.fractions or 0
            return feet * 12 + inches + fractions
        else:
            raise ValueError('Unable to give a Sort Value')

    # @property
    # def format_padded_value(self):
    #     """
    #     Pad results with minutes and feet even if there are none
    #     """
    #     """
    #     tmp = timedelta(
    #         minutes=minutes or 0,
    #         seconds=seconds or 0,
    #         milliseconds=subsecond or 0,
    #     )
    #     tmp_min = tmp.seconds // 60
    #     tmp_sec = tmp.seconds % 60
    #     tmp_microseconds = tmp.microseconds
    #     tmp_format = f"{tmp_min}:{tmp_sec}.{tmp_microseconds}"
    #     print(f"tmp: {tmp}, tmp_min: {tmp_min}, tmp_sec: {tmp_sec}, tmp_microseconds: {tmp_microseconds}, tmp_format: {tmp_format}")

    #     """
    #     if self.minutes or self.seconds or self.subsecond:
    #         minutes = self.minutes or 0
    #         seconds = self.seconds or 0
    #         subsecond = self.subsecond or 0
    #         return minutes * 60 + seconds + subsecond
    #     elif self.feet or self.inches or self.fractions:
    #         feet = self.feet or 0
    #         inches = self.inches or 0
    #         fractions = self.fractions or 0
    #         return feet * 12 + inches + fractions
    #     else:
    #         raise ValueError('Unable to give a Sort Value')

    @property
    def put(self):
        output = f"{self.event_str}::{self.result_str}"
        return output

    @property
    def sort_value(self):
        if self.minutes or self.seconds or self.subsecond:
            minutes = self.minutes or 0
            seconds = self.seconds or 0
            subsecond = self.subsecond or 0
            return minutes * 60 + seconds + subsecond
        elif self.feet or self.inches or self.fractions:
            feet = self.feet or 0
            inches = self.inches or 0
            fractions = self.fractions or 0
            return feet * 12 + inches + fractions
        else:
            raise ValueError('Unable to give a Sort Value')

    @classmethod
    def build(cls, input):
        event, result = input.split('::')
        return cls.parse_event_result(event=event, result=result)

    def __gt__(self, other):
        if self.seconds is not None and self.subsecond is not None and other.seconds is not None and other.subsecond is not None:
            self_time = [
                self.minutes or 0,
                self.seconds or 0,
                self.subsecond or 0
            ]
            self_time = timedelta(minutes=self_time[0], seconds=self_time[1], milliseconds=self_time[2] * 1000)
            other_time = [
                other.minutes or 0,
                other.seconds or 0,
                other.subsecond or 0
            ]
            other_time = timedelta(minutes=other_time[0], seconds=other_time[1], milliseconds=other_time[2] * 1000)
            if self_time < other_time:
                return True
            else:
                return False
        elif self.inches is not None and self.fractions is not None and other.inches is not None and other.fractions is not None:
            self_distance = [
                self.feet or 0,
                self.inches or 0,
                self.fractions or 0
            ]
            self_distance = self_distance[0] * 12 + self_distance[1] + self_distance[2]
            other_distance = [
                other.feet or 0,
                other.inches or 0,
                other.fractions or 0
            ]
            other_distance = other_distance[0] * 12 + other_distance[1] + other_distance[2]
            if self_distance < other_distance:
                return False
            else:
                return True
        else:
            print(f"event_str: {self.event_str}, {other.event_str}")
            print(f"result_str: {self.result_str}, {other.result_str}")
            print(f"minutes: {self.minutes}, {other.minutes}")
            print(f"seconds: {self.seconds}, {other.seconds}")
            print(f"subsecond: {self.subsecond}, {other.subsecond}")
            print(f"feet: {self.feet}, {other.feet}")
            print(f"inches: {self.inches}, {other.inches}")
            print(f"fractions: {self.fractions}, {other.fractions}")
            raise ValueError('Invalid Result')


class ResultData(BaseModel):
    uid: str
    update_datetime: datetime

    event: str
    heat: int
    place: int
    wind: float
    athlete: AthleteData | None = None
    athlete_uid: str | None = None
    team: str | None = None
    meet_date: datetime
    result: Result
    meet: str
    gender: str | None = None
    points: float | None = None

    result_metadata: Dict[str, Any] | None = None

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


class ResultApiCreate(BaseModel):
    event: str
    heat: int
    place: int
    wind: float | None = None
    athlete_uid: str | None = None
    athlete_first_name: str | None = None
    athlete_last_name: str | None = None
    team: str | None = None
    meet_date: datetime
    result: Result
    meet: str
    gender: str | None = None
    points: float | None = None

    result_metadata: Dict[str, Any] | None = None

    athlete: AthleteData | None = None


    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if not fields.get('wind'):
            fields['wind'] = 0.0
        fields['athlete'] = None
        result = Result.parse_event_result(event=fields['event'], result=fields['result'])
        fields['result'] = result
        fields['gender'] = EventParser.parse_event_gender(event_s=fields['event'])
        if not any([fields.get('athlete_uid'), fields.get('athlete_first_name'), fields.get('athlete_last_name')]):
            raise ValueError("Must provide either athlete_uid or athlete_first_name and athlete_last_name")
        return fields

    def cast_data_object(self) -> ResultData:
        """Return a data object based on the ResultData class"""
        content = self.model_dump()
        content['uid'] = str(uuid4())
        content['update_datetime'] = datetime.now(timezone.utc)
        data_obj = ResultData(**content)
        return data_obj

    @property
    def put(self):
        output = self.model_dump()
        return output


class ResultDBBase(SQLModel):
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
    result: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
    meet: str
    gender: str | None = None
    points: float | None = None

    result_metadata: str | None = None

    search_team: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        return fields

    def cast_data_object(self) -> ResultData:
        """Return a data object based on the ResultData class"""
        content = self.model_dump()
        content['result_metadata'] = json.loads(content['result_metadata'])
        data_obj = ResultData(**content)
        return data_obj


class ResultDBCreate(ResultDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if not isinstance(fields, dict):
            fields = fields.model_dump()
        fields['athlete_uid'] = fields['athlete']['uid']
        fields['search_team'] = fields['team'].lower()
        fields['result_metadata'] = json.dumps(fields['result_metadata'])
        return fields


class ResultDBRead(ResultDBBase):
    pass


class ResultDB(ResultDBBase, table=True):
    __tablename__ = "result"


class ResultFilter(BaseModel):
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
    points: List[str] = []

    meet_date: List[str] = []
    # result: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))

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
            fields['team'] = [t.lower().strip() for t in team]

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
            if fields['gender'] == ['All']:
                fields['gender'] = []

        if fields.get('meet_date'):
            meet_date = []
            [meet_date.extend(i.split(',')) for i in fields['meet_date']]
            fields['meet_date'] = [m.strip() for m in meet_date]

        if fields.get('points'):
            points = []
            [points.extend(i.split(',')) for i in fields['points']]
            fields['points'] = [f.strip() for f in points]

        if fields.get('sort'):
            order_by = fields.get('order_by', [])
            for sort in fields['sort']:
                for item in sort.split(','):
                    if not item or item in ['-', 'None', 'null', None]:
                        continue
                    order_by.append(item.lower())
            fields['order_by'] = order_by

        # if isinstance(fields.get('active'), list):
        #     fields['active'] = fields['active'][0]
        if isinstance(fields.get('limit'), list):
            fields['limit'] = fields['limit'][0]
        if isinstance(fields.get('offset'), list):
            fields['offset'] = fields['offset'][0]
        return fields

    def apply_filters(self, database_object_class: ResultDBBase, query: select, count: bool = False) -> select:
        """Apply the filters to the query"""
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
            filter_list = [database_object_class.search_team.contains(t) for t in self.team]
            query = query.filter(or_(*filter_list))

        if self.meet:
            filter_list = [database_object_class.meet.contains(m) for m in self.meet]
            query = query.filter(or_(*filter_list))

        # if self.first_name:
        #     filter_list = [database_object_class.first_name.contains(f) for f in self.first_name]
        #     query = query.filter(or_(*filter_list))

        # if self.last_name:
        #     filter_list = [database_object_class.last_name.contains(l) for l in self.last_name]
        #     query = query.filter(or_(*filter_list))

        if self.athlete_uid:
            filter_list = [database_object_class.athlete_uid.contains(a) for a in self.athlete_uid]
            query = query.filter(or_(*filter_list))

        if self.gender:
            filter_list = [database_object_class.gender.contains(g) for g in self.gender]
            query = query.filter(or_(*filter_list))

        if self.meet_date:
            for meet_date in self.meet_date:
                if meet_date.startswith('Is on'):
                    query = query.filter(database_object_class.meet_date == datetime.strptime(meet_date[5:], "%Y-%m-%d"))
                elif meet_date.startswith('After'):
                    query = query.filter(database_object_class.meet_date >= datetime.strptime(meet_date[5:], "%Y-%m-%d"))
                elif meet_date.startswith('Before'):
                    query = query.filter(database_object_class.meet_date <= datetime.strptime(meet_date[6:], "%Y-%m-%d"))

        if not count:
            if self.limit:
                query = query.limit(self.limit)
            for order_by in self.order_by:
                query = query.order_by(getattr(database_object_class, order_by))
            if self.offset:
                query = query.offset(self.offset)

        return query

    def count_applicable(self, database_object_class: ResultDBBase, query: select) -> select:
        count = query
        x=1
