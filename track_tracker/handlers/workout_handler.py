from bdb import GENERATOR_AND_COROUTINE_FLAGS
import json
from datetime import datetime
from sqlmodel import Session, select, func

from .base_handler import BaseHandler
from models import (
    WorkoutData,
    WorkoutApiCreate,
    WorkoutDBBase,
    WorkoutDBCreate,
    WorkoutDBRead,
    WorkoutDB,
    WorkoutFilter,
)
from html import display_date
from html.common import class_formatter
from html.env import SEASON_YEAR

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class WorkoutHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_workout(self, workout: WorkoutData) -> WorkoutData:
        self.context.logger.info(f"Creating workout: {workout.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            create_obj = WorkoutDBCreate.model_validate(workout)
            create_obj = WorkoutDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = WorkoutDBRead.model_validate(create_obj)
            workout = read_obj.cast_data_object()
        self.context.logger.info(f"Workout Created: {workout.model_dump_json()}")
        return workout

    async def filter_workouts(self, workout_filter: WorkoutFilter) -> list[WorkoutData]:
        self.context.logger.info(f"Filtering workouts: {workout_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(WorkoutDB)
            query = workout_filter.apply_filters(WorkoutDB, query)
            rows = session.exec(query).all()
            workouts = []
            for row in rows:
                read_obj = WorkoutDBRead.model_validate(row)
                workout = read_obj.cast_data_object()
                workouts.append(workout)
        self.context.logger.info(f"Workouts Filtered: {len(workouts)}")
        return workouts

    async def find_workouts(self, workout_filter: WorkoutFilter, silence_missing=False) -> WorkoutData:
        """
        Find single matching workout or error
        """
        self.context.logger.info(f"Filtering workouts: {workout_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(WorkoutDB)
            query = workout_filter.apply_filters(WorkoutDB, query)
            rows = session.exec(query).all()
            workouts = []
            for row in rows:
                read_obj = WorkoutDBRead.model_validate(row)
                workout = read_obj.cast_data_object()
                workouts.append(workout)
            if len(workouts) == 0:
                if silence_missing:
                    return None
                raise MissingRecordException(f"No records found for filter: [{workout_filter.model_dump_json()}]")
            elif len(workouts) > 1:
                raise DuplicateRecordsException(f"Multiple records found for filter: [{workout_filter.model_dump_json()}]")
            else:
                workout = workouts[0]
        self.context.logger.info(f"Workout found")
        return workout

    # async def filter_workouts_display(self, workout_filter: WorkoutFilter) -> list[dict]:
    #     self.context.logger.info(f"Filtering workouts for display: {workout_filter.model_dump_json()}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(WorkoutDB)
    #         query = workout_filter.apply_filters(WorkoutDB, query)
    #         rows = session.exec(query).all()
    #         workouts = []
    #         for row in rows:
    #             read_obj = WorkoutDBRead.model_validate(row)
    #             workout = read_obj.cast_data_object()
    #             workouts.append(workout)

    #         # COUNT DOESNT WORK IF THERE ARE FILTERS APPLIED. IT ONLY GETS MAX SIZE FOR ALL RECORDS
    #         query_max_count = select(func.count(WorkoutDB.uid))
    #         query_max_count = workout_filter.apply_filters(WorkoutDB, query_max_count, count=True)
    #         query_max_count = session.exec(
    #             query_max_count).one()

    #         # query_max_count = rows = session.exec(
    #         #     select(func.count(WorkoutDB.uid))).one()

    #     self.context.logger.info(f"Workouts Filtered: {len(workouts)}")
    #     display_workouts = []
    #     for workout in workouts:
    #         athlete = workout.athlete_uid

    #         display_workouts.append({
    #             'Event': workout.event,
    #             'Place': workout.place,
    #             'MSAthlete': athlete,
    #             'Team': workout.team,
    #             'Workout': workout.workout.format,
    #             'Wind': workout.wind,
    #             'Heat': workout.heat,
    #             'Class': SEASON_YEAR,
    #             'Meet': workout.meet,
    #             'Date': display_date(workout.meet_date),
    #             'Gender': workout.gender,
    #         })
    #     return display_workouts, query_max_count
