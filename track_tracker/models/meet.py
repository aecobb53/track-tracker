from datetime import datetime, timezone, date, time
import json
from typing import List, Dict, Any
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from sqlmodel import or_, and_
from pydantic import BaseModel, model_validator
from enum import Enum
from uuid import uuid4

# from .common import apply_modifier
from .event import EventParser
from .result import Result


class MeetEventAthlete(BaseModel):
    first_name: str
    last_name: str
    team: str | None = None
    graduation_year: int | None = None

    flight: int | None = None
    heat: int | None = None
    lane: int | None = None
    seed: Result | None = None

    place: int | None = None
    wind: float | None = None
    result: Result | None = None
    points: int | None = None

    result_is_pr: bool | None = None

    meet_metadata: Dict[str, Any] = {}

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def place_in_lineup(self):
        ep = EventParser(self.result.event_str)
        if ep.event_type == 'run':
            output = f"Heat {self.heat}"
            if self.lane:
                output += f" Lane {self.lane}"
            return output.strip()
        elif ep.event_type == 'throw':
            output = f"Flight {self.flight}"
            if self.lane:
                output += f" Thrower {self.lane}"
            return output.strip()
        elif ep.event_type == 'jump':
            output = f"Flight {self.flight}"
            if self.lane:
                output += f" Jumper {self.lane}"
            return output.strip()
        elif ep.event_type == 'vault':
            output = f"Flight {self.flight}"
            if self.lane:
                output += f" Vaulter {self.lane}"
            return output.strip()

    @property
    def to_json(self):
        output = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'name': self.name,
            'team': self.team,
            'graduation_year': self.graduation_year,
            'seed': self.seed.to_json if self.seed else None,
            'flight': self.flight,
            'heat': self.heat,
            'lane': self.lane,
            'place_in_lineup': self.place_in_lineup,
            'place': self.place,
            'points': self.points,
            'wind': self.wind,
            'result': self.result.to_json if self.result else None,
            'result_is_pr': self.result_is_pr,
            'meet_metadata': self.meet_metadata,
        }
        return output

    @classmethod
    def from_json(cls, data):
        content = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'team': data['team'],
            'graduation_year': data['graduation_year'],
            'seed': Result.from_json(data['seed']) if data.get('seed') else None,
            'flight': data['flight'],
            'heat': data['heat'],
            'lane': data['lane'],
            'place': data['place'],
            'points': data['points'],
            'wind': data['wind'],
            'result': Result.from_json(data['result']) if data.get('result') else None,
            'result_is_pr': data['result_is_pr'],
            'meet_metadata': data['meet_metadata'],
        }
        obj = cls(**content)
        return obj


class MeetEventAthleteAPICreate(BaseModel):
    first_name: str
    last_name: str
    team: str | None = None
    graduation_year: int | None = None

    flight: int | None = None
    heat: int | None = None
    lane: int | None = None
    seed: Result | None = None

    place: int | None = None
    wind: float | None = None
    result: Result | None = None

    meet_metadata: Dict[str, Any] = {}

    event_name: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields.get('result') and fields.get('event_name'):
            result = Result.parse_event_result(event=fields['event_name'], result=fields['result'])
            fields['result'] = Result.parse_event_result(event=fields['event_name'], result=fields['result'])
        elif fields.get('result') or fields.get('event_name'):
            # I need both to be useful
            pass
        return fields

    def cast_data_object(self) -> MeetEventAthlete:
        """Return a data object based on the MeetEventAthlete class"""
        content = self.model_dump()
        data_obj = MeetEventAthlete(**content)
        return data_obj


class MeetEvent(BaseModel):
    event_name: str
    event_time: time | None = None
    gender: str | None = None

    athletes: List[MeetEventAthlete] = []

    is_relay: bool = False
    meet_metadata: Dict[str, Any] = {}

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if not fields.get('gender'):
            try:
                fields['gender'] = EventParser.parse_event_gender(fields['event_name'])
            except Exception as e:
                pass
        if not fields.get('is_relay'):
            try:
                fields['is_relay'] = EventParser.parse_event_is_relay(fields['event_name'])
            except Exception as e:
                pass
        return fields


    @property
    def to_json(self):
        output = {
            'event_name': self.event_name,
            'gender': self.gender,
            'is_relay': self.is_relay,
            'athletes': [a.to_json for a in self.athletes],
            'meet_metadata': self.meet_metadata,
        }
        if self.event_time:
            # output['event_time'] = str(self.event_time)
            output['event_time'] = self.event_time.isoformat()
        return output

    @classmethod
    def from_json(cls, data):
        content = {
            'event_name': data['event_name'],
            'gender': data['gender'],
            'is_relay': data['is_relay'],
            'athletes': [MeetEventAthlete.from_json(a) for a in data['athletes']],
            'meet_metadata': data['meet_metadata'],
        }
        if data.get('event_time'):
            content['event_time'] = datetime.strptime(data['event_time'], "%H:%M:%S").time()
        obj = cls(**content)
        return obj


class Meet(BaseModel):
    uid: str
    update_datetime: datetime

    meet_name: str
    meet_location: str | None = None
    meet_date: date | None = None

    events: List[MeetEvent] = []

    varsity_points: bool = True
    small_meet: bool = False
    max_school_scores: int | None = None
    meet_point_values: list[int] | None = None
    meet_metadata: Dict[str, Any] = {}

    @property
    def put(self):
        output = self.model_dump()
        return output

    @property
    def rest_output(self):
        output = self.model_dump_json()
        return output

    @property
    def to_json(self):
        output = {
            'uid': self.uid,
            'update_datetime': self.update_datetime.isoformat(),
            'meet_name': self.meet_name,
            'meet_location': self.meet_location,
            'meet_date': self.meet_date.isoformat() if self.meet_date else None,
            'events': [e.to_json for e in self.events],
            'varsity_points': self.varsity_points,
            'small_meet': self.small_meet,
            'max_school_scores': self.max_school_scores,
            'meet_point_values': self.meet_point_values,
            'meet_metadata': self.meet_metadata,
        }
        return output

    @classmethod
    def from_json(cls, data):
        content = {
            'uid': data['uid'],
            # 'update_datetime': data['update_datetime'],
            'meet_name': data['meet_name'],
            'meet_location': data['meet_location'],
            # 'meet_date': data['meet_date'],
            'events': [MeetEvent.from_json(e) for e in data['events']],
            'varsity_points': data['varsity_points'],
            'small_meet': data['small_meet'],
            'max_school_scores': data['max_school_scores'],
            'meet_point_values': data['meet_point_values'],
            'meet_metadata': data['meet_metadata'],
        }
        if data.get('update_datetime'):
            # content['update_datetime'] = datetime.strptime(data['update_datetime'], "%Y-%m-%dT%H:%M:%S.%fZ")
            content['update_datetime'] = datetime.fromisoformat(data['update_datetime'])
        if data.get('meet_date'):
            content['meet_date'] = datetime.strptime(data['meet_date'], "%Y-%m-%d").date()
        # if data.get('event_time'):
        #     content['event_time'] = datetime.strftime(data['event_time'], "%H:%M:%S").time()
        obj = cls(**content)
        return obj


class MeetApiCreate(BaseModel):
    meet_name: str
    meet_location: str | None = None
    meet_date: date | None = None

    events: List[MeetEvent] = []

    varsity_points: bool = True
    small_meet: bool = False
    max_school_scores: int | None = 3
    meet_metadata: Dict[str, Any] = {}

    auto_populate_events: bool = True
    meet_point_values: list[int] | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields.get('meet_name'):
            fields['meet_name'] = fields['meet_name'].strip()
        if fields.get('meet_location'):
            fields['meet_location'] = fields['meet_location'].strip()
        if fields.get('meet_date'):
            fields['meet_date'] = datetime.strptime(fields['meet_date'], "%Y-%m-%d").date()
        if not fields.get('meet_point_values'):
            if fields.get('varsity_points', True):
                if fields.get('small_meet'):
                    fields['meet_point_values'] = [5, 3, 1]
                else:
                    fields['meet_point_values'] = [10, 8, 6, 5, 4, 3, 2, 1]
            else:
                fields['meet_point_values'] = None
        return fields

    def cast_data_object(self) -> Meet:
        """Return a data object based on the Meet class"""
        content = self.model_dump()
        content['uid'] = str(uuid4())
        content['update_datetime'] = datetime.now(timezone.utc)
        data_obj = Meet(**content)
        return data_obj


# class MeetDBBase(SQLModel):
#     id: int | None = Field(primary_key=True, default=None)
#     uid: str = Field(unique=True)
#     update_datetime: datetime | None = None

#     meet_name: str | None = None
#     meet_location: str | None = None
#     meet_date: date | None = None

#     events: str | None = None

#     varsity_points: bool = True
#     small_meet: bool = False
#     meet_metadata: str | None = None

#     def cast_data_object(self) -> Meet:
#         """Return a data object based on the Meet class"""
#         content = self.model_dump()
#         # content['events']
#         # content['tags'] = json.loads(self.tags)
#         content['meet_metadata'] = json.loads(self.meet_metadata)
#         data_obj = Meet(**content)
#         return data_obj


# class MeetDBCreate(MeetDBBase):
#     @model_validator(mode='before')
#     def validate_fields(cls, fields):
#         fields = fields.model_dump()
#         fields['meet_metadata'] = json.dumps(fields['meet_metadata'])
#         return fields


# class MeetDBRead(MeetDBBase):
#     pass


# class MeetDB(MeetDBBase, table=True):
#     __tablename__ = "meet"


# class MeetFilter(BaseModel):
#     uid: List[str] | None = None

#     first_name: List[str] | None = None
#     last_name: List[str] | None = None

#     first_name_only: List[str] | None = None
#     last_name_only: List[str] | None = None
#     first_nickname_only: List[str] | None = None
#     last_nickname_only: List[str] | None = None

#     team: List[str] | None = None
#     gender: List[str] | None = None
#     graduation_year: List[str] | None = None

#     current: List[str] | None = None
#     event_class: str | None = None
#     tags: List[str] | None = None

#     # active: bool = True

#     limit: int = 1000
#     order_by: List[str] = ['last_name', 'first_name']
#     offset: int = 0

#     @model_validator(mode='before')
#     def validate_fields(cls, fields):
#         if fields.get('first_name'):
#             first_name = []
#             [first_name.extend(i.lower().split(',')) for i in fields['first_name']]
#             fields['first_name'] = [e.strip() for e in first_name]

#         if fields.get('last_name'):
#             last_name = []
#             [last_name.extend(i.lower().split(',')) for i in fields['last_name']]
#             fields['last_name'] = [e.strip() for e in last_name]

#         if fields.get('first_name_only'):
#             first_name_only = []
#             [first_name_only.extend(i.lower().split(',')) for i in fields['first_name_only']]
#             fields['first_name_only'] = [e.strip() for e in first_name_only]

#         if fields.get('last_name_only'):
#             last_name_only = []
#             [last_name_only.extend(i.lower().split(',')) for i in fields['last_name_only']]
#             fields['last_name_only'] = [e.strip() for e in last_name_only]

#         if fields.get('first_nickname_only'):
#             first_nickname_only = []
#             [first_nickname_only.extend(i.lower().split(',')) for i in fields['first_nickname_only']]
#             fields['first_nickname_only'] = [e.strip() for e in first_nickname_only]

#         if fields.get('last_nickname_only'):
#             last_nickname_only = []
#             [last_nickname_only.extend(i.lower().split(',')) for i in fields['last_nickname_only']]
#             fields['last_nickname_only'] = [e.strip() for e in last_nickname_only]

#         if fields.get('team'):
#             team = []
#             [team.extend(i.lower().split(',')) for i in fields['team']]
#             fields['team'] = [e.strip() for e in team]

#         if fields.get('gender'):
#             gender = []
#             [gender.extend(i.split(',')) for i in fields['gender']]
#             fields['gender'] = [g.strip() for g in gender]
#             if fields['gender'] == ['All']:
#                 fields['gender'] = []

#         if fields.get('current'):
#             if fields['current'] == ['Current']:
#                 year = datetime.now(timezone.utc).year
#                 fields['graduation_year'] = [f"Greater than or equal to{year}", f"Less than or equal to{year+3}"]

#         if fields.get('event_class'):
#             event_class = fields.pop('event_class')
#             if event_class == ['All']:
#                 del event_class
#             else:
#                 tags = []
#                 for ec in event_class:
#                     tags.extend(ec.split(','))
#                 if 'tags' not in fields:
#                     fields['tags'] = []
#                 fields['tags'].extend(tags)

#         if fields.get('graduation_year'):
#             graduation_year = []
#             for i in fields['graduation_year']:
#                 i_l = i.split(',')
#                 for ii in i_l:
#                     ii = ii.strip()
#                     if ii:
#                         graduation_year.append(ii)
#             fields['graduation_year'] = graduation_year

#         if fields.get('sort'):
#             order_by = fields.get('order_by', [])
#             for sort in fields['sort']:
#                 for item in sort.split(','):
#                     if not item or item in ['-', 'None', 'null', None]:
#                         continue
#                     order_by.append(item.replace(' ', '_').lower())
#             fields['order_by'] = order_by

#         # if isinstance(fields.get('active'), list):
#         #     fields['active'] = fields['active'][0]
#         if isinstance(fields.get('limit'), list):
#             fields['limit'] = fields['limit'][0]
#         if isinstance(fields.get('offset'), list):
#             fields['offset'] = fields['offset'][0]
#         return fields

#     def apply_filters(self, database_object_class: MeetDBBase, query: select, count: bool = False) -> select:
#         """Apply the filters to the query"""
#         if self.uid:
#             query = query.filter(database_object_class.uid.in_(self.uid))

#         if self.first_name:
#             filter_list = [database_object_class.search_first_name.contains(e) for e in self.first_name]
#             filter_list + [database_object_class.search_first_nickname.contains(e) for e in self.first_name]
#             query = query.filter(or_(*filter_list))

#         if self.last_name:
#             filter_list = [database_object_class.search_last_name.contains(e) for e in self.last_name]
#             filter_list + [database_object_class.search_last_nickname.contains(e) for e in self.last_name]
#             query = query.filter(or_(*filter_list))

#         if self.first_name_only:
#             filter_list = [database_object_class.search_first_name.contains(e) for e in self.first_name_only]
#             query = query.filter(or_(*filter_list))

#         if self.last_name_only:
#             filter_list = [database_object_class.search_last_name.contains(e) for e in self.last_name_only]
#             query = query.filter(or_(*filter_list))

#         if self.first_nickname_only:
#             filter_list = [database_object_class.search_first_nickname.contains(e) for e in self.first_nickname_only]
#             query = query.filter(or_(*filter_list))

#         if self.last_nickname_only:
#             filter_list = [database_object_class.search_last_nickname.contains(e) for e in self.last_nickname_only]
#             query = query.filter(or_(*filter_list))

#         if self.team:
#             filter_list = [database_object_class.search_team.contains(e) for e in self.team]
#             query = query.filter(or_(*filter_list))

#         if self.tags:
#             filter_list = [database_object_class.tags.contains(e) for e in self.tags]
#             query = query.filter(or_(*filter_list))

#         if self.graduation_year:
#             filter_list = []
#             for graduation_year in self.graduation_year:
#                 query = apply_modifier(query, database_object_class.graduation_year, graduation_year)

#         if self.gender:
#             filter_list = [database_object_class.gender.contains(g) for g in self.gender]
#             query = query.filter(or_(*filter_list))

#         if not count:
#             if self.limit:
#                 query = query.limit(self.limit)
#             for order_by in self.order_by:
#                 query = query.order_by(getattr(database_object_class, order_by))
#             if self.offset:
#                 query = query.offset(self.offset)

#         return query

#     # def add_current_students_for_year(self, year):
#     #     print(f"ADdING STUDENTS ACTIVE IN {year}")
#     #     x=1
