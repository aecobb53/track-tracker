import json
from datetime import datetime
from sqlmodel import Session, select, func

from .base_handler import BaseHandler
from models import (
    ResultData,
    ResultApiCreate,
    ResultDBBase,
    ResultDBCreate,
    ResultDBRead,
    ResultDB,
    ResultFilter,
)
from html import display_date

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class ResultHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_result(self, result: ResultData) -> ResultData:
        self.context.logger.info(f"Creating result: {result.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            create_obj = ResultDBCreate.model_validate(result)
            create_obj = ResultDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = ResultDBRead.model_validate(create_obj)
            result = read_obj.cast_data_object()
        self.context.logger.info(f"Result Created: {result.model_dump_json()}")
        return result

    async def filter_results(self, result_filter: ResultFilter) -> list[ResultData]:
        self.context.logger.info(f"Filtering results: {result_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(ResultDB)
            query = result_filter.apply_filters(ResultDB, query)
            rows = session.exec(query).all()
            results = []
            for row in rows:
                read_obj = ResultDBRead.model_validate(row)
                result = read_obj.cast_data_object()
                results.append(result)
        self.context.logger.info(f"Results Filtered: {len(results)}")
        return results

    async def find_results(self, result_filter: ResultFilter, silence_missing=False) -> ResultData:
        """
        Find single matching result or error
        """
        self.context.logger.info(f"Filtering results: {result_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(ResultDB)
            query = result_filter.apply_filters(ResultDB, query)
            rows = session.exec(query).all()
            results = []
            for row in rows:
                read_obj = ResultDBRead.model_validate(row)
                result = read_obj.cast_data_object()
                results.append(result)
            if len(results) == 0:
                if silence_missing:
                    return None
                raise MissingRecordException(f"No records found for filter: [{result_filter.model_dump_json()}]")
            elif len(results) > 1:
                raise DuplicateRecordsException(f"Multiple records found for filter: [{result_filter.model_dump_json()}]")
            else:
                result = results[0]
        self.context.logger.info(f"Result found")
        return result

    async def filter_results_display(self, result_filter: ResultFilter) -> list[dict]:
        self.context.logger.info(f"Filtering results for display: {result_filter.model_dump_json()}")
        with Session(self.context.database.engine) as session:
            query = select(ResultDB)
            query = result_filter.apply_filters(ResultDB, query)
            rows = session.exec(query).all()
            results = []
            for row in rows:
                read_obj = ResultDBRead.model_validate(row)
                result = read_obj.cast_data_object()
                results.append(result)

            # COUNT DOESNT WORK IF THERE ARE FILTERS APPLIED. IT ONLY GETS MAX SIZE FOR ALL RECORDS
            query_max_count = select(func.count(ResultDB.uid))
            query_max_count = result_filter.apply_filters(ResultDB, query_max_count, count=True)
            query_max_count = session.exec(
                query_max_count).one()

            # query_max_count = rows = session.exec(
            #     select(func.count(ResultDB.uid))).one()

        self.context.logger.info(f"Results Filtered: {len(results)}")
        display_results = []
        for result in results:
            athlete = result.athlete_uid

            display_results.append({
                'Event': result.event,
                'Place': result.place,
                'Athlete': athlete,
                'Team': result.team,
                'Result': result.result.format,
                'Wind': result.wind,
                'Heat': result.heat,
                'Meet': result.meet,
                'Date': display_date(result.meet_date),
                'Gender': result.gender,
            })
        return display_results, query_max_count

    # async def find_result(self, result_uid: str) -> Result:
    #     self.context.logger.info(f"Finding result: {result_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(ResultDB)
    #         query = query.where(ResultDB.uid == result_uid)
    #         row = session.exec(query).first()
    #         if row is None:
    #             raise MissingRecordException(f"No records found for uid: [{result_uid}]")
    #         read_obj = ResultDBRead.model_validate(row)
    #         result = read_obj.cast_data_object(Result)
    #     self.context.logger.info(f"Result found: [{result_uid}]")
    #     return result

    # async def update_result(self, result_uid: str, result: Result) -> Result:
    #     self.context.logger.info(f"Updating result: {result_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(ResultDB)
    #         query = query.where(ResultDB.uid == result_uid)
    #         row = session.exec(query).first()
    #         if row is None:
    #             raise MissingRecordException(f"No records found for uid: [{result_uid}]")

    #         # Verify data integrity
    #         immutable_fields = [
    #             'uid',
    #             'creation_datetime',
    #         ]
    #         immutable_modification_detected = []
    #         for key in immutable_fields:
    #             if getattr(row, key) != getattr(result, key):
    #                 immutable_modification_detected.append(key)
    #         if len(immutable_modification_detected) > 0:
    #             raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

    #         # Make changes
    #         skip_fields = [
    #             'geometry',
    #         ]
    #         for key in Result.__fields__.keys():
    #             if key not in skip_fields:
    #                 try:
    #                     if getattr(row, key) != getattr(result, key):
    #                         setattr(row, key, getattr(result, key))
    #                 except AttributeError:
    #                     pass
    #         row.update_datetime = datetime.utcnow()
    #         session.add(row)
    #         session.commit()
    #         session.refresh(row)
    #         read_obj = ResultDBRead.model_validate(row)
    #         result = read_obj.cast_data_object(Result)
    #     self.context.logger.info(f"Result updated: [{result_uid}]")
    #     return result

    # async def set_activation(self, result_uid: str, active_state: bool) -> Result:
    #     self.context.logger.debug(f"Setting Result activation: [{result_uid}] to [{active_state}]")

    #     result = await self.find_result(result_uid=result_uid)
    #     result.active = active_state
    #     result = await self.update_result(result_uid=result_uid, result=result)

    #     self.context.logger.info(f"Set result activation: [{result.uid}]")
    #     return result

    # async def delete_result(self, result_uid: str) -> None:
    #     self.context.logger.info(f"Deleting result: {result_uid}")
    #     with Session(self.context.database.engine) as session:
    #         query = select(ResultDB)
    #         query = query.where(ResultDB.uid == result_uid)
    #         row = session.exec(query).first()
    #         session.delete(row)
    #         session.commit()
    #     self.context.logger.info(f"Result deleted")
