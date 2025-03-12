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
from .result import Result


class WorkoutData(BaseModel):
    uid: str
    update_datetime: datetime

    # Athlete
    athlete: AthleteData | None = None
    athlete_uid: str | None = None

    # Result
    # results: Dict = []
    results: Dict[str, Result | str] = {}

    # Drill
    workout: str
    workout_description: str | None = None
    workout_date: datetime | None = None

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


class WorkoutApiCreate(BaseModel):
    # Result
    # results: Dict
    results: Dict[str, Result | str] = {}

    # Drill
    workout: str
    workout_description: str | None = None
    workout_date: datetime | None = None

    athlete_uid: str | None = None
    athlete_first_name: str | None = None
    athlete_last_name: str | None = None
    athlete: AthleteData | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields['athlete'] = None
        results = {}
        for key, result in fields['results'].items():
            try:
                result = Result.parse_event_result(event=fields['workout'], result=result)
            except:
                pass
            results[key] = result
        # for result in fields['results']:
        #     result = Result.parse_event_result(event=result['workout'], result=result['result'])
        #     results.append(result)
        # # results = Result.parse_event_result(event=fields['event'], result=fields['result'])
        fields['results'] = results
        if not any([fields.get('athlete_uid'), fields.get('athlete_first_name'), fields.get('athlete_last_name')]):
            raise ValueError("Must provide either athlete_uid or athlete_first_name and athlete_last_name")
        return fields

    def cast_data_object(self) -> WorkoutData:
        """Return a data object based on the WorkoutData class"""
        content = self.model_dump()
        content['uid'] = str(uuid4())
        content['update_datetime'] = datetime.now(timezone.utc)
        data_obj = WorkoutData(**content)
        return data_obj

    @property
    def put(self):
        output = self.model_dump()
        return output


class WorkoutDBBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    uid: str = Field(unique=True)
    update_datetime: datetime | None = None

    athlete_uid: str = Field(foreign_key="athlete.uid")
    results: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))

    workout: str
    workout_description: str | None = None
    workout_date: datetime | None = None

    search_workout: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        return fields

    def cast_data_object(self) -> WorkoutData:
        """Return a data object based on the WorkoutData class"""
        content = self.model_dump()
        data_obj = WorkoutData(**content)
        return data_obj


class WorkoutDBCreate(WorkoutDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if not isinstance(fields, dict):
            fields = fields.model_dump()
        fields['athlete_uid'] = fields['athlete']['uid']
        fields['search_workout'] = fields['workout'].lower()
        return fields


class WorkoutDBRead(WorkoutDBBase):
    pass


class WorkoutDB(WorkoutDBBase, table=True):
    __tablename__ = "workout"


class WorkoutFilter(BaseModel):
    uid: List[str] | None = None

    workout: List[str] = []
    athlete_uid: List[str] = []

    workout_date: List[str] = []

    limit: int = 1000
    order_by: List[str] = ['workout_date']
    offset: int = 0


    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields.get('workout'):
            workout = []
            [workout.extend(i.split(',')) for i in fields['workout']]
            fields['workout'] = [w.strip() for w in workout]

        # if fields.get('athlete_name'):
            # athlete_name = []
            # # [athlete_name.extend(i.split(',')) for i in fields['athlete_name']]
            # # fields['athlete_name'] = [w.strip() for w in athlete_name]

        if fields.get('workout_date'):
            workout_date = []
            [workout_date.extend(i.split(',')) for i in fields['workout_date']]
            fields['workout_date'] = [w.strip() for w in workout_date]

        # if fields.get('sort'):
        #     order_by = fields.get('order_by', [])
        #     for sort in fields['sort']:
        #         for item in sort.split(','):
        #             if not item or item in ['-', 'None', 'null', None]:
        #                 continue
        #             order_by.append(item.lower())
        #     fields['order_by'] = order_by

        # if isinstance(fields.get('active'), list):
        #     fields['active'] = fields['active'][0]
        if isinstance(fields.get('limit'), list):
            fields['limit'] = fields['limit'][0]
        if isinstance(fields.get('offset'), list):
            fields['offset'] = fields['offset'][0]
        return fields

    def apply_filters(self, database_object_class: WorkoutDBBase, query: select, count: bool = False) -> select:
        """Apply the filters to the query"""
        if self.uid:
            query = query.filter(database_object_class.uid.in_(self.uid))

        if self.athlete_uid:
            query = query.filter(database_object_class.athlete_uid.in_(self.athlete_uid))

        if self.workout:
            filter_list = [database_object_class.workout.contains(w) for w in self.workout]
            query = query.filter(or_(*filter_list))

        if self.workout_date:
            for workout_date in self.workout_date:
                if workout_date.startswith('Is on'):
                    query = query.filter(database_object_class.workout_date == datetime.strptime(workout_date[5:], "%Y-%m-%d"))
                elif workout_date.startswith('After'):
                    query = query.filter(database_object_class.workout_date >= datetime.strptime(workout_date[5:], "%Y-%m-%d"))
                elif workout_date.startswith('Before'):
                    query = query.filter(database_object_class.workout_date <= datetime.strptime(workout_date[6:], "%Y-%m-%d"))

        if not count:
            if self.limit:
                query = query.limit(self.limit)
            for order_by in self.order_by:
                query = query.order_by(getattr(database_object_class, order_by))
            if self.offset:
                query = query.offset(self.offset)

        return query

    # def count_applicable(self, database_object_class: WorkoutDBBase, query: select) -> select:
    #     count = query
    #     x=1
