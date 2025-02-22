from fastapi import APIRouter, HTTPException, Request, Response, Depends

# from models import Mark, MarkFilter
# # from handlers import MarkHandler
from handlers import AthleteHandler, MarkHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
# # from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
# from models import MarkData, MarkApiCreate, MarkFilter
from models import MarkData, MarkApiCreate, MarkFilter, AthleteFilter
from models import ContextSingleton

from typing import Annotated

context = ContextSingleton()

router = APIRouter(
    prefix='/mark',
    tags=['mark'],
)


@router.post('/', status_code=201)
async def create_mark(mark: MarkApiCreate):
    try:
        ah = AthleteHandler()
        athlete = await ah.find_athlete(AthleteFilter(
            first_name=[mark.athlete_first_name],
            last_name=[mark.athlete_last_name],
            team=[mark.team],
        ))
        mark.athlete = athlete
        mark_data = mark.cast_data_object()
        mh = MarkHandler()

        existing_mark_filter = MarkFilter(
            event=[mark_data.event],
            athlete_uid=[mark.athlete.uid],
            team=[mark_data.team],
            meet=[mark_data.meet],
        )
        existing_mark = await mh.find_marks(mark_filter=existing_mark_filter, silence_missing=True)
        if existing_mark:
            # Verify the record doesnt already exist
            raise DuplicateRecordsException(f"event={mark_data.event}, athlete_uid={mark.athlete.uid}, team={mark_data.team}")
        created_mark = await mh.create_mark(mark=mark_data)
        return created_mark.put
    except MissingRecordException as err:
        message = f"No record found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=404, detail=message)
    except DuplicateRecordsException as err:
        message = f"Duplicate records found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/', status_code=200)
async def filter_mark(request: Request):
    try:
        mark_filter = parse_query_params(request=request, query_class=MarkFilter)
        mh = MarkHandler()
        marks = await mh.filter_marks(mark_filter=mark_filter)
        ah = AthleteHandler()
        for mark in marks:
            athlete = await ah.find_athlete(AthleteFilter(uid=[mark.athlete_uid]))
            mark.athlete = athlete
        return {'marks': marks}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.put('/', status_code=200)
async def update_mark(mark: MarkData):
    try:
        mh = AthleteHandler()
        created_mark = await mh.update_mark(mark=mark)
        return created_mark.put
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/display', status_code=200)
async def filter_mark(request: Request):
    try:
        mark_filter = parse_query_params(request=request, query_class=MarkFilter)
        mh = MarkHandler()
        marks = await mh.filter_marks_display(mark_filter=mark_filter)
        ah = AthleteHandler()
        for mark in marks:
            athlete = await ah.find_athlete(AthleteFilter(uid=[mark['Athlete']]))
            mark['Athlete'] = f"{athlete.first_name} {athlete.last_name}"
        return marks
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


# @router.put('/{mark_id}', status_code=200)
# async def update_mark(mark_id: str, mark: Mark):
#     rh = MarkHandler()
#     try:
#         updated_mark = await rh.update_mark(mark_uid=mark_id, mark=mark)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     # except DuplicateRecordsException as err:
#     #     message = f"Duplicate records found: [{err}]"
#     #     context.logger.error(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_mark


# @router.get('/{mark_id}', status_code=200)
# async def find_mark(mark_id: str):
#     rh = MarkHandler()
#     try:
#         mark = await rh.find_mark(mark_uid=mark_id)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     # except DuplicateRecordsException as err:
#     #     message = f"Duplicate records found: [{err}]"
#     #     context.logger.error(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return mark


# @router.put('/{mark_id}/activate', status_code=200)
# async def activate_mark(mark_id: str):
#     rh = MarkHandler()
#     try:
#         updated_mark = await rh.set_activation(mark_uid=mark_id, active_state=True)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_mark


# @router.put('/{mark_id}/deactivate', status_code=200)
# async def deactivate_mark(mark_id: str):
#     rh = MarkHandler()
#     try:
#         updated_mark = await rh.set_activation(mark_uid=mark_id, active_state=False)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_mark


# @router.delete('/{mark_id}', status_code=200)
# async def delete_mark(mark_id: str):
#     rh = MarkHandler()
#     try:
#         updated_mark = await rh.delete_mark(mark_uid=mark_id)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_mark
