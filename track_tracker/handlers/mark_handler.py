import json
from datetime import datetime
from sqlmodel import Session, select

from .base_handler import BaseHandler
from models import (
    MarkData,
    MarkApiCreate,
    MarkDBBase,
    MarkDBCreate,
    MarkDBRead,
    MarkDB,
    MarkFilter,
)

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class MarkHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_mark(self, mark: MarkData) -> MarkData:
        self.context.logger.info(f"Creating mark: {mark.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            create_obj = MarkDBCreate.model_validate(mark)
            create_obj = MarkDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = MarkDBRead.model_validate(create_obj)
            mark = read_obj.cast_data_object()
        self.context.logger.info(f"Mark Created: {mark.model_dump_json()}")
        return mark

    async def filter_marks(self, mark_filter: MarkFilter) -> list[MarkData]:
        self.context.logger.info(f"Filtering marks: {mark_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(MarkDB)
            query = mark_filter.apply_filters(MarkDB, query)
            rows = session.exec(query).all()
            marks = []
            for row in rows:
                read_obj = MarkDBRead.model_validate(row)
                mark = read_obj.cast_data_object()
                marks.append(mark)
        self.context.logger.info(f"Marks Filtered: {len(marks)}")
        return marks

    # async def find_mark(self, mark_uid: str) -> Mark:
    #     self.context.logger.info(f"Finding mark: {mark_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(MarkDB)
    #         query = query.where(MarkDB.uid == mark_uid)
    #         row = session.exec(query).first()
    #         if row is None:
    #             raise MissingRecordException(f"No records found for uid: [{mark_uid}]")
    #         read_obj = MarkDBRead.model_validate(row)
    #         mark = read_obj.cast_data_object(Mark)
    #     self.context.logger.info(f"Mark found: [{mark_uid}]")
    #     return mark

    # async def update_mark(self, mark_uid: str, mark: Mark) -> Mark:
    #     self.context.logger.info(f"Updating mark: {mark_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(MarkDB)
    #         query = query.where(MarkDB.uid == mark_uid)
    #         row = session.exec(query).first()
    #         if row is None:
    #             raise MissingRecordException(f"No records found for uid: [{mark_uid}]")

    #         # Verify data integrity
    #         immutable_fields = [
    #             'uid',
    #             'creation_datetime',
    #         ]
    #         immutable_modification_detected = []
    #         for key in immutable_fields:
    #             if getattr(row, key) != getattr(mark, key):
    #                 immutable_modification_detected.append(key)
    #         if len(immutable_modification_detected) > 0:
    #             raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

    #         # Make changes
    #         skip_fields = [
    #             'geometry',
    #         ]
    #         for key in Mark.__fields__.keys():
    #             if key not in skip_fields:
    #                 try:
    #                     if getattr(row, key) != getattr(mark, key):
    #                         setattr(row, key, getattr(mark, key))
    #                 except AttributeError:
    #                     pass
    #         row.update_datetime = datetime.utcnow()
    #         session.add(row)
    #         session.commit()
    #         session.refresh(row)
    #         read_obj = MarkDBRead.model_validate(row)
    #         mark = read_obj.cast_data_object(Mark)
    #     self.context.logger.info(f"Mark updated: [{mark_uid}]")
    #     return mark

    # async def set_activation(self, mark_uid: str, active_state: bool) -> Mark:
    #     self.context.logger.debug(f"Setting Mark activation: [{mark_uid}] to [{active_state}]")

    #     mark = await self.find_mark(mark_uid=mark_uid)
    #     mark.active = active_state
    #     mark = await self.update_mark(mark_uid=mark_uid, mark=mark)

    #     self.context.logger.info(f"Set mark activation: [{mark.uid}]")
    #     return mark

    # async def delete_mark(self, mark_uid: str) -> None:
    #     self.context.logger.info(f"Deleting mark: {mark_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(MarkDB)
    #         query = query.where(MarkDB.uid == mark_uid)
    #         row = session.exec(query).first()
    #         session.delete(row)
    #         session.commit()
    #     self.context.logger.info(f"Mark deleted")
