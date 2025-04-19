from datetime import datetime, timezone
import json
from typing import List, Dict, Any
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from sqlmodel import or_, and_
from pydantic import BaseModel, model_validator
from enum import Enum
from uuid import uuid4

from .event import EventParser
from .common import apply_modifier


class AthleteData(BaseModel):
    uid: str
    update_datetime: datetime

    first_name: str | None = None
    last_name: str | None = None
    team: str | None = None
    gender: str | None = None
    graduation_year: int | None = None

    aliases: List[str] = []
    tags: List[str] = []
    active: bool = True

    athlete_metadata: Dict[str, Any] = {}

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
        # output['aliases'] = self.aliases
        # output['tags'] = self.tags
        return output

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __eq__(self, other_object):
        if self.uid != other_object.uid:
            return False
        if self.update_datetime != other_object.update_datetime:
            return False
        if self.first_name != other_object.first_name:
            return False
        if self.last_name != other_object.last_name:
            return False
        if self.team != other_object.team:
            return False
        if self.gender != other_object.gender:
            return False
        if self.graduation_year != other_object.graduation_year:
            return False
        if self.aliases != other_object.aliases:
            return False
        if self.tags != other_object.tags:
            return False
        if self.active != other_object.active:
            return False
        if self.athlete_metadata != other_object.athlete_metadata:
            return False
        return True



class AthleteApiCreate(BaseModel):
    first_name: str
    last_name: str
    graduation_year: int | None = None
    team: str
    gender: str | None = None

    aliases: List[str] = []
    tags: List[str] = []

    athlete_metadata: Dict[str, Any] = {}

    def cast_data_object(self) -> AthleteData:
        """Return a data object based on the AthleteData class"""
        content = self.model_dump()
        content['uid'] = str(uuid4())
        content['update_datetime'] = datetime.now(timezone.utc)
        content['active'] = True
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

    search_first_name: str | None = None
    search_last_name: str | None = None
    search_team: str | None = None

    aliases: str | None = None
    tags: str | None = None
    active: bool | None = True

    athlete_metadata: str | None = None

    def cast_data_object(self) -> AthleteData:
        """Return a data object based on the AthleteData class"""
        content = self.model_dump()
        content['aliases'] = json.loads(self.aliases)
        content['tags'] = json.loads(self.tags)
        content['athlete_metadata'] = json.loads(self.athlete_metadata)
        data_obj = AthleteData(**content)
        return data_obj


class AthleteDBCreate(AthleteDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = fields.model_dump()
        fields['search_first_name'] = fields['first_name'].lower()
        fields['search_last_name'] = fields['last_name'].lower()
        fields['search_team'] = fields['team'].lower()
        fields['aliases'] = json.dumps(fields['aliases'])
        fields['tags'] = json.dumps(list(set(fields['tags'])))
        fields['athlete_metadata'] = json.dumps(fields['athlete_metadata'])
        return fields


class AthleteDBRead(AthleteDBBase):
    pass


class AthleteDB(AthleteDBBase, table=True):
    __tablename__ = "athlete"


class AthleteFilter(BaseModel):
    uid: List[str] | None = None

    first_name: List[str] | None = None
    last_name: List[str] | None = None
    # aliases: List[str] | None = None
    team: List[str] | None = None
    gender: List[str] | None = None
    graduation_year: List[str] | None = None

    current: List[str] | None = None
    event_class: str | None = None
    tags: List[str] | None = None

    # active: bool

    limit: int = 1000
    order_by: List[str] = ['last_name', 'first_name']
    offset: int = 0

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields.get('first_name'):
            first_name = []
            [first_name.extend(i.lower().split(',')) for i in fields['first_name']]
            fields['first_name'] = [e.strip() for e in first_name]

        if fields.get('last_name'):
            last_name = []
            [last_name.extend(i.lower().split(',')) for i in fields['last_name']]
            fields['last_name'] = [e.strip() for e in last_name]

        if fields.get('team'):
            team = []
            [team.extend(i.lower().split(',')) for i in fields['team']]
            fields['team'] = [e.strip() for e in team]

        if fields.get('gender'):
            gender = []
            [gender.extend(i.split(',')) for i in fields['gender']]
            fields['gender'] = [g.strip() for g in gender]
            if fields['gender'] == ['All']:
                fields['gender'] = []

        if fields.get('current'):
            if fields['current'] == ['Current']:
                year = datetime.now(timezone.utc).year
                fields['graduation_year'] = [f"Greater than or equal to{year}", f"Less than or equal to{year+3}"]

        if fields.get('event_class'):
            event_class = fields.pop('event_class')
            if event_class == ['All']:
                del event_class
            else:
                tags = []
                for ec in event_class:
                    tags.extend(ec.split(','))
                if 'tags' not in fields:
                    fields['tags'] = []
                fields['tags'].extend(tags)

        if fields.get('graduation_year'):
            graduation_year = []
            for i in fields['graduation_year']:
                i_l = i.split(',')
                for ii in i_l:
                    ii = ii.strip()
                    if ii:
                        graduation_year.append(ii)
            fields['graduation_year'] = graduation_year

        if fields.get('sort'):
            order_by = fields.get('order_by', [])
            for sort in fields['sort']:
                for item in sort.split(','):
                    if not item or item in ['-', 'None', 'null', None]:
                        continue
                    order_by.append(item.replace(' ', '_').lower())
            fields['order_by'] = order_by

        # if isinstance(fields.get('active'), list):
        #     fields['active'] = fields['active'][0]
        if isinstance(fields.get('limit'), list):
            fields['limit'] = fields['limit'][0]
        if isinstance(fields.get('offset'), list):
            fields['offset'] = fields['offset'][0]
        return fields

    def apply_filters(self, database_object_class: AthleteDBBase, query: select, count: bool = False) -> select:
        """Apply the filters to the query"""
        if self.uid:
            query = query.filter(database_object_class.uid.in_(self.uid))

        if self.first_name:
            filter_list = [database_object_class.search_first_name.contains(e) for e in self.first_name]
            query = query.filter(or_(*filter_list))

        if self.last_name:
            filter_list = [database_object_class.search_last_name.contains(e) for e in self.last_name]
            query = query.filter(or_(*filter_list))

        if self.team:
            filter_list = [database_object_class.search_team.contains(e) for e in self.team]
            query = query.filter(or_(*filter_list))

        if self.tags:
            filter_list = [database_object_class.tags.contains(e) for e in self.tags]
            query = query.filter(or_(*filter_list))

        if self.graduation_year:
            filter_list = []
            for graduation_year in self.graduation_year:
                query = apply_modifier(query, database_object_class.graduation_year, graduation_year)

        if self.gender:
            filter_list = [database_object_class.gender.contains(g) for g in self.gender]
            query = query.filter(or_(*filter_list))

        if not count:
            if self.limit:
                query = query.limit(self.limit)
            for order_by in self.order_by:
                query = query.order_by(getattr(database_object_class, order_by))
            if self.offset:
                query = query.offset(self.offset)

        return query

    # def add_current_students_for_year(self, year):
    #     print(f"ADdING STUDENTS ACTIVE IN {year}")
    #     x=1
