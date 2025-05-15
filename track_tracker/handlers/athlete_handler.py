import json
from datetime import datetime
from sqlmodel import Session, select, func

from .base_handler import BaseHandler
from models import (
    MSAthleteData,
    MSAthleteApiCreate,
    MSAthleteDBBase,
    MSAthleteDBCreate,
    MSAthleteDBRead,
    MSAthleteDB,
    MSAthleteFilter,
)
from html import display_date
from html.common import class_formatter

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class MSAthleteHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_athlete(self, athlete: MSAthleteData) -> MSAthleteData:
        self.context.logger.info(f"Creating athlete: {athlete.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            create_obj = MSAthleteDBCreate.model_validate(athlete)
            create_obj = MSAthleteDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = MSAthleteDBRead.model_validate(create_obj)
            athlete = read_obj.cast_data_object()
        self.context.logger.info(f"MSAthlete Created: {athlete.model_dump_json()}")
        return athlete

    async def filter_athletes(self, athlete_filter: MSAthleteFilter) -> list[MSAthleteData]:
        """
        Return matching athletes
        """
        # self.context.logger.info(f"Filtering athletes: {athlete_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(MSAthleteDB)
            query = athlete_filter.apply_filters(MSAthleteDB, query)
            rows = session.exec(query).all()
            athletes = []
            for row in rows:
                read_obj = MSAthleteDBRead.model_validate(row)
                athlete = read_obj.cast_data_object()
                athletes.append(athlete)
        # self.context.logger.info(f"MSAthletes Filtered: {len(athletes)}")
        return athletes

    async def find_athlete(self, athlete_filter: MSAthleteFilter, silence_missing=False, silence_dupe=False) -> MSAthleteData:
        """
        Find single matching athlete or error
        """
        # self.context.logger.info(f"Filtering athletes: {athlete_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(MSAthleteDB)
            query = athlete_filter.apply_filters(MSAthleteDB, query)
            rows = session.exec(query).all()
            athletes = []
            for row in rows:
                read_obj = MSAthleteDBRead.model_validate(row)
                athlete = read_obj.cast_data_object()
                athletes.append(athlete)
            if len(athletes) == 0:
                if silence_missing:
                    return None
                raise MissingRecordException(f"No records found for filter: [{athlete_filter.model_dump_json()}]")
            elif len(athletes) > 1:
                if silence_dupe:
                    athlete = athletes[0]
                else:
                    raise DuplicateRecordsException(f"Multiple records found for filter: [{athlete_filter.model_dump_json()}]")
            else:
                athlete = athletes[0]
        # self.context.logger.info(f"MSAthlete found")
        return athlete

    async def update_athlete(self, athlete: MSAthleteData) -> MSAthleteData:
        self.context.logger.info(f"Updating athlete: {athlete.uid}")
        with Session(self.context.database.engine) as session:
            query = select(MSAthleteDB)
            query = query.where(MSAthleteDB.uid == athlete.uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No records found for uid: [{athlete.uid}]")

            skip_fields = ("uid", "update_datetime")

            for key in MSAthleteData.__fields__.keys():
                if key not in skip_fields:
                    try:
                        if key in ['aliases', 'tags', 'athlete_metadata']:
                            setattr(athlete, key, json.dumps(getattr(athlete, key)))
                        if getattr(row, key) != getattr(athlete, key):
                            setattr(row, key, getattr(athlete, key))
                    except AttributeError:
                        pass
            row.update_datetime = datetime.utcnow()
            session.add(row)
            session.commit()
            session.refresh(row)
            read_obj = MSAthleteDBRead.model_validate(row)
            athlete = read_obj.cast_data_object()
        self.context.logger.info(f"MSAthlete updated: [{athlete.uid}]")
        return athlete

    async def filter_athletes_display(self, athlete_filter: MSAthleteFilter) -> list[dict]:
        # self.context.logger.info(f"Filtering athletes for display: {athlete_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(MSAthleteDB)
            query = athlete_filter.apply_filters(MSAthleteDB, query)
            rows = session.exec(query).all()
            athletes = []
            for row in rows:
                read_obj = MSAthleteDBRead.model_validate(row)
                athlete = read_obj.cast_data_object()
                athletes.append(athlete)

            query_max_count = select(func.count(MSAthleteDB.uid))
            query_max_count = athlete_filter.apply_filters(MSAthleteDB, query_max_count, count=True)
            query_max_count = session.exec(
                query_max_count).one()

        # self.context.logger.info(f"MSAthletes Filtered: {len(athletes)}")
        display_athletes = []
        for athlete in athletes:
            results = {}
            records = {}
            display_athletes.append({
                'First Name': athlete.first_name,
                'Last Name': athlete.last_name,
                'Nickname': athlete.aliases,
                'Event Class': athlete.tags,
                'Team': athlete.team,
                'Gender': athlete.gender,
                'Class': class_formatter(athlete.graduation_year, allow_none=True)[0],
                'results': results,
                'records': records,
                'uid': athlete.uid,
            })
        return display_athletes, query_max_count

    async def delete_athlete(self, athlete_uid: str) -> MSAthleteData:
        self.context.logger.info(f"Deleting athlete: {athlete_uid}")
        with Session(self.context.database.engine) as session:
            query = select(MSAthleteDB)
            query = query.where(MSAthleteDB.uid == athlete_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No records found for uid: [{athlete_uid}]")

            session.delete(row)
            session.commit()
            read_obj = MSAthleteDBRead.model_validate(row)
            athlete = read_obj.cast_data_object()
        self.context.logger.info(f"MSAthlete deleted: [{athlete_uid}]")
        return athlete


    # async def set_activation(self, athlete_uid: str, active_state: bool) -> MSAthlete:
    #     self.context.logger.debug(f"Setting MSAthlete activation: [{athlete_uid}] to [{active_state}]")

    #     athlete = await self.find_athlete(athlete_uid=athlete_uid)
    #     athlete.active = active_state
    #     athlete = await self.update_athlete(athlete_uid=athlete_uid, athlete=athlete)

    #     self.context.logger.info(f"Set athlete activation: [{athlete.uid}]")
    #     return athlete

    # async def delete_athlete(self, athlete_uid: str) -> None:
    #     self.context.logger.info(f"Deleting athlete: {athlete_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(MSAthleteDB)
    #         query = query.where(MSAthleteDB.uid == athlete_uid)
    #         row = session.exec(query).first()
    #         session.delete(row)
    #         session.commit()
    #     self.context.logger.info(f"MSAthlete deleted")
