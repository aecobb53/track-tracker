import os
import json
from datetime import datetime
from sqlmodel import Session, select, func

# from .base_handler import BaseHandler
from .base_file_handler import BaseFileHandler
from models import (
    MeetEvent,
    Meet,
)
from html import display_date
from html.common import class_formatter

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class MeetHandler(BaseFileHandler):
    def __init__(self, meet_name: str, *args, **kwargs):
        self.file_name = f'meet_{meet_name}.json'
        super().__init__(file_name=self.file_name, file_directory='meet', *args, **kwargs)

        self.content = {}

    def save_file(self):
        self._saved_content = self.content.to_json  # Convert from pydantic to JSON
        super().save_file()

    def load_file(self):
        super().load_file()
        # self.content = self._saved_content  # Convert from JSON to pydantic
        self.content = Meet.from_json(self._saved_content)  # Convert from JSON to pydantic
        return self.content

    def move_file(self, new_directory: str):
        """
        Move the file to a new name
        """
        old_file_path = self.file_path
        self.file_directory = new_directory
        new_file_path = self.file_path
        self._ensure_directory()
        os.rename(old_file_path, new_file_path)

    def add_event(self, event: MeetEvent):
        """
        Add an event to the meet
        event_name: str
        event: dict - or eventually a pydantic object
        """
        self.load_file()
        for event_item in self.content.events:
            if event.event_name == event_item.event_name:
                raise DuplicateRecordsException(f"Event {event.event_name} already exists in meet {self.content.meet_name}")
        self.content.events.append(event)

    def find_event(self, event_name: str = None, event_index: int = None):
        self.load_file()
        if event_name:
            for index, event in enumerate(self.content.events):
                if event.event_name == event_name:
                    return event, index
            else:
                raise MissingRecordException(f"Event {event_name} does not exist in meet {self.content.meet_name}")
        elif event_index:
            if event_index < len(self.content.events):
                return event.events[event_index], event_index
            else:
                raise MissingRecordException(f"Event index {event_index} does not exist in meet {self.content.meet_name}")
        return None, None

    def update_event(self, event_name: str, event: MeetEvent):
        """
        Update an event in the meet
        event_name: str
        event: dict - or eventually a pydantic object
        """
        self.load_file()
        _, event_index = self.find_event(event_name=event_name)
        self.content.events[event_index] = event
        self.save_file()

    def move_event(self, new_event_index: int, event_name: str = None, event_index: int = None):
        """
        Update an event in the meet
        event_name: str
        event: dict - or eventually a pydantic object
        """
        self.load_file()
        _, event_index = self.find_event(event_name=event_name)
        event = self.content.events.pop(event_index)
        try:
            # Try to add the popped event to a new index
            self.content.events.insert(new_event_index, event)
            self.save_file()
        except Exception as e:
            # Try to add the popped event to the old index (or just dont save?)
            self.content.events.insert(event_index, event)
            raise DataIntegrityException(f"Event {event.event_name} cannot be moved to index {new_event_index} in meet {self.content.meet_name}") from e
        # self.save_file()

    def delete_event(self, event_name: str):
        """
        Delete an event from the meet
        event_name: str
        """
        self.load_file()
        for event_index in range(len(self.content.events)):
            if self.content.events[event_index].event_name == event_name:
                self.content.events.pop(event_index)
                break
        else:
            raise MissingRecordException(f"Event {event_name} does not exist in meet {self.content.meet_name}")


# mh = MeetHandler(meet_name="Testing Meet")
# mh.content = {
#     "meet_name": "Example Meet",
#     "meet_date": "2023-10-01",
#     "location": "Example Location",
# }
# mh.save_file()

#     async def create_athlete(self, athlete: MSAthleteData) -> MSAthleteData:
#         self.context.logger.info(f"Creating athlete: {athlete.model_dump_json()}")
#         with Session(self.context.database.engine) as session:
#             create_obj = MSAthleteDBCreate.model_validate(athlete)
#             create_obj = MSAthleteDB.model_validate(create_obj)
#             session.add(create_obj)
#             session.commit()
#             session.refresh(create_obj)
#             read_obj = MSAthleteDBRead.model_validate(create_obj)
#             athlete = read_obj.cast_data_object()
#         self.context.logger.info(f"MSAthlete Created: {athlete.model_dump_json()}")
#         return athlete

#     async def filter_athletes(self, athlete_filter: MSAthleteFilter) -> list[MSAthleteData]:
#         """
#         Return matching athletes
#         """
#         # self.context.logger.info(f"Filtering athletes: {athlete_filter.model_dump_json()}")
#         with Session(self.context.database.engine) as session:
#             query = select(MSAthleteDB)
#             query = athlete_filter.apply_filters(MSAthleteDB, query)
#             rows = session.exec(query).all()
#             athletes = []
#             for row in rows:
#                 read_obj = MSAthleteDBRead.model_validate(row)
#                 athlete = read_obj.cast_data_object()
#                 athletes.append(athlete)
#         # self.context.logger.info(f"MSAthletes Filtered: {len(athletes)}")
#         return athletes

#     async def find_athlete(self, athlete_filter: MSAthleteFilter, silence_missing=False, silence_dupe=False) -> MSAthleteData:
#         """
#         Find single matching athlete or error
#         """
#         # self.context.logger.info(f"Filtering athletes: {athlete_filter.model_dump_json()}")
#         with Session(self.context.database.engine) as session:
#             query = select(MSAthleteDB)
#             query = athlete_filter.apply_filters(MSAthleteDB, query)
#             rows = session.exec(query).all()
#             athletes = []
#             for row in rows:
#                 read_obj = MSAthleteDBRead.model_validate(row)
#                 athlete = read_obj.cast_data_object()
#                 athletes.append(athlete)
#             if len(athletes) == 0:
#                 if silence_missing:
#                     return None
#                 raise MissingRecordException(f"No records found for filter: [{athlete_filter.model_dump_json()}]")
#             elif len(athletes) > 1:
#                 if silence_dupe:
#                     athlete = athletes[0]
#                 else:
#                     raise DuplicateRecordsException(f"Multiple records found for filter: [{athlete_filter.model_dump_json()}]")
#             else:
#                 athlete = athletes[0]
#         # self.context.logger.info(f"MSAthlete found")
#         return athlete

#     async def update_athlete(self, athlete: MSAthleteData) -> MSAthleteData:
#         self.context.logger.info(f"Updating athlete: {athlete.uid}")
#         with Session(self.context.database.engine) as session:
#             query = select(MSAthleteDB)
#             query = query.where(MSAthleteDB.uid == athlete.uid)
#             row = session.exec(query).first()
#             if row is None:
#                 raise MissingRecordException(f"No records found for uid: [{athlete.uid}]")

#             skip_fields = ("uid", "update_datetime")

#             for key in MSAthleteData.__fields__.keys():
#                 if key not in skip_fields:
#                     try:
#                         if key in ['aliases', 'tags', 'athlete_metadata']:
#                             setattr(athlete, key, json.dumps(getattr(athlete, key)))
#                         if getattr(row, key) != getattr(athlete, key):
#                             setattr(row, key, getattr(athlete, key))
#                     except AttributeError:
#                         pass
#             row.update_datetime = datetime.utcnow()
#             session.add(row)
#             session.commit()
#             session.refresh(row)
#             read_obj = MSAthleteDBRead.model_validate(row)
#             athlete = read_obj.cast_data_object()
#         self.context.logger.info(f"MSAthlete updated: [{athlete.uid}]")
#         return athlete

#     async def filter_athletes_display(self, athlete_filter: MSAthleteFilter) -> list[dict]:
#         # self.context.logger.info(f"Filtering athletes for display: {athlete_filter.model_dump_json()}")
#         with Session(self.context.database.engine) as session:
#             query = select(MSAthleteDB)
#             query = athlete_filter.apply_filters(MSAthleteDB, query)
#             rows = session.exec(query).all()
#             athletes = []
#             for row in rows:
#                 read_obj = MSAthleteDBRead.model_validate(row)
#                 athlete = read_obj.cast_data_object()
#                 athletes.append(athlete)

#             query_max_count = select(func.count(MSAthleteDB.uid))
#             query_max_count = athlete_filter.apply_filters(MSAthleteDB, query_max_count, count=True)
#             query_max_count = session.exec(
#                 query_max_count).one()

#         # self.context.logger.info(f"MSAthletes Filtered: {len(athletes)}")
#         display_athletes = []
#         for athlete in athletes:
#             results = {}
#             records = {}
#             display_athletes.append({
#                 'First Name': athlete.first_name,
#                 'Last Name': athlete.last_name,
#                 'Nickname': athlete.aliases,
#                 'Event Class': athlete.tags,
#                 'Team': athlete.team,
#                 'Gender': athlete.gender,
#                 'Class': class_formatter(athlete.graduation_year, allow_none=True)[0],
#                 'results': results,
#                 'records': records,
#                 'uid': athlete.uid,
#             })
#         return display_athletes, query_max_count

#     async def delete_athlete(self, athlete_uid: str) -> MSAthleteData:
#         self.context.logger.info(f"Deleting athlete: {athlete_uid}")
#         with Session(self.context.database.engine) as session:
#             query = select(MSAthleteDB)
#             query = query.where(MSAthleteDB.uid == athlete_uid)
#             row = session.exec(query).first()
#             if row is None:
#                 raise MissingRecordException(f"No records found for uid: [{athlete_uid}]")

#             session.delete(row)
#             session.commit()
#             read_obj = MSAthleteDBRead.model_validate(row)
#             athlete = read_obj.cast_data_object()
#         self.context.logger.info(f"MSAthlete deleted: [{athlete_uid}]")
#         return athlete


#     # async def set_activation(self, athlete_uid: str, active_state: bool) -> MSAthlete:
#     #     self.context.logger.debug(f"Setting MSAthlete activation: [{athlete_uid}] to [{active_state}]")

#     #     athlete = await self.find_athlete(athlete_uid=athlete_uid)
#     #     athlete.active = active_state
#     #     athlete = await self.update_athlete(athlete_uid=athlete_uid, athlete=athlete)

#     #     self.context.logger.info(f"Set athlete activation: [{athlete.uid}]")
#     #     return athlete

#     # async def delete_athlete(self, athlete_uid: str) -> None:
#     #     self.context.logger.info(f"Deleting athlete: {athlete_uid}")
#     #     with Session(self.context.database.engine) as session:
#     #         query = select(MSAthleteDB)
#     #         query = query.where(MSAthleteDB.uid == athlete_uid)
#     #         row = session.exec(query).first()
#     #         session.delete(row)
#     #         session.commit()
#     #     self.context.logger.info(f"MSAthlete deleted")
