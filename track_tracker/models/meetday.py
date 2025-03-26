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


class Meet(BaseModel):
    name: str
    events: list
    data_time_version: str | None = None
    run_full_update: bool = True#False

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        # print(f"FIELDS: {fields}")
        if not fields.get('events'):
            fields['events'] = []
        return fields



class MeetDay(BaseModel):
    date: str
    name: str
    csv: list

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        print(f"FIELDS: {fields}")
        if not fields.get('csv'):
            fields['csv'] = []
        return fields
