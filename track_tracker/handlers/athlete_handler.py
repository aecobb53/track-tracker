import json
from datetime import datetime
from sqlmodel import Session, select

from .base_handler import BaseHandler
from models import (
    AthleteData,
    AthleteApiCreate,
    AthleteDBBase,
    AthleteDBCreate,
    AthleteDBRead,
    AthleteDB,
    AthleteFilter,
)

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class AthleteHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_athlete(self, athlete: AthleteData) -> AthleteData:
        self.context.logger.info(f"Creating athlete: {athlete.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            create_obj = AthleteDBCreate.model_validate(athlete)
            create_obj = AthleteDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = AthleteDBRead.model_validate(create_obj)
            athlete = read_obj.cast_data_object()
        self.context.logger.info(f"Athlete Created: {athlete.model_dump_json()}")
        return athlete

    async def filter_athletes(self, athlete_filter: AthleteFilter) -> list[AthleteData]:
        self.context.logger.info(f"Filtering athletes: {athlete_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(AthleteDB)
            query = athlete_filter.apply_filters(AthleteDB, query)
            rows = session.exec(query).all()
            athletes = []
            for row in rows:
                read_obj = AthleteDBRead.model_validate(row)
                athlete = read_obj.cast_data_object()
                athletes.append(athlete)
        self.context.logger.info(f"Athletes Filtered: {len(athletes)}")
        return athletes

    # async def find_athlete(self, athlete_uid: str) -> Athlete:
    #     self.context.logger.info(f"Finding athlete: {athlete_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(AthleteDB)
    #         query = query.where(AthleteDB.uid == athlete_uid)
    #         row = session.exec(query).first()
    #         if row is None:
    #             raise MissingRecordException(f"No records found for uid: [{athlete_uid}]")
    #         read_obj = AthleteDBRead.model_validate(row)
    #         athlete = read_obj.cast_data_object(Athlete)
    #     self.context.logger.info(f"Athlete found: [{athlete_uid}]")
    #     return athlete

    # async def update_athlete(self, athlete_uid: str, athlete: Athlete) -> Athlete:
    #     self.context.logger.info(f"Updating athlete: {athlete_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(AthleteDB)
    #         query = query.where(AthleteDB.uid == athlete_uid)
    #         row = session.exec(query).first()
    #         if row is None:
    #             raise MissingRecordException(f"No records found for uid: [{athlete_uid}]")

    #         # Verify data integrity
    #         immutable_fields = [
    #             'uid',
    #             'creation_datetime',
    #         ]
    #         immutable_modification_detected = []
    #         for key in immutable_fields:
    #             if getattr(row, key) != getattr(athlete, key):
    #                 immutable_modification_detected.append(key)
    #         if len(immutable_modification_detected) > 0:
    #             raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

    #         # Make changes
    #         skip_fields = [
    #             'geometry',
    #         ]
    #         for key in Athlete.__fields__.keys():
    #             if key not in skip_fields:
    #                 try:
    #                     if getattr(row, key) != getattr(athlete, key):
    #                         setattr(row, key, getattr(athlete, key))
    #                 except AttributeError:
    #                     pass
    #         row.update_datetime = datetime.utcnow()
    #         session.add(row)
    #         session.commit()
    #         session.refresh(row)
    #         read_obj = AthleteDBRead.model_validate(row)
    #         athlete = read_obj.cast_data_object(Athlete)
    #     self.context.logger.info(f"Athlete updated: [{athlete_uid}]")
    #     return athlete

    # async def set_activation(self, athlete_uid: str, active_state: bool) -> Athlete:
    #     self.context.logger.debug(f"Setting Athlete activation: [{athlete_uid}] to [{active_state}]")

    #     athlete = await self.find_athlete(athlete_uid=athlete_uid)
    #     athlete.active = active_state
    #     athlete = await self.update_athlete(athlete_uid=athlete_uid, athlete=athlete)

    #     self.context.logger.info(f"Set athlete activation: [{athlete.uid}]")
    #     return athlete

    # async def delete_athlete(self, athlete_uid: str) -> None:
    #     self.context.logger.info(f"Deleting athlete: {athlete_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(AthleteDB)
    #         query = query.where(AthleteDB.uid == athlete_uid)
    #         row = session.exec(query).first()
    #         session.delete(row)
    #         session.commit()
    #     self.context.logger.info(f"Athlete deleted")
