from fastapi import APIRouter, HTTPException, Request, Response, Depends

# from models import Result, MSResultFilter
# # from handlers import MSResultHandler
from handlers import MSAthleteHandler, MSResultHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
# # from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
# from models import MSResultData, MSResultApiCreate, MSResultFilter
from models import MSResultData, MSResultApiCreate, MSResultFilter, MSAthleteFilter
from models import ContextSingleton

from typing import Annotated
from html.common import class_formatter

context = ContextSingleton()

router = APIRouter(
    prefix='/result',
    tags=['result'],
)


@router.post('/', status_code=201)
async def create_result(result: MSResultApiCreate):
    try:
        ah = MSAthleteHandler()
        athlete = await ah.find_athlete(MSAthleteFilter(
            first_name=[result.athlete_first_name],
            last_name=[result.athlete_last_name],
            team=[result.team],
        ))
        result.athlete = athlete
        result_data = result.cast_data_object()
        mh = MSResultHandler()

        existing_result_filter = MSResultFilter(
            event=[result_data.event],
            athlete_uid=[result.athlete.uid],
            team=[result_data.team],
            meet=[result_data.meet],
        )
        existing_result = await mh.find_results(result_filter=existing_result_filter, silence_missing=True)
        if existing_result:
            # Verify the record doesnt already exist
            raise DuplicateRecordsException(f"event={result_data.event}, athlete_uid={result.athlete.uid}, team={result_data.team}")
        created_result = await mh.create_result(result=result_data)
        return created_result.put
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
async def filter_result(request: Request):
    try:
        result_filter = parse_query_params(request=request, query_class=MSResultFilter)
        ah = MSAthleteHandler()
        if result_filter.first_name or result_filter.last_name and not result_filter.athlete_uid:
            athlete_filter = MSAthleteFilter(
                first_name=result_filter.first_name,
                last_name=result_filter.last_name,
            )
            athlete = await ah.find_athlete(athlete_filter, silence_missing=True)
            if athlete:
                result_filter.athlete_uid = [athlete.uid]
        mh = MSResultHandler()
        results = await mh.filter_results(result_filter=result_filter)
        for result in results:
            athlete = await ah.find_athlete(MSAthleteFilter(uid=[result.athlete_uid]))
            result.athlete = athlete
        return {'results': results}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.put('/', status_code=200)
async def update_result(result: MSResultData):
    try:
        mh = MSResultHandler()
        created_result = await mh.update_result(result=result)
        return created_result.put
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.delete('/{result_uid}', status_code=200)
async def delete_result(result_uid: str):
    try:
        mh = MSResultHandler()
        created_result = await mh.delete_result(result_uid=result_uid)
        return created_result.put
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/display', status_code=200)
async def filter_result(request: Request):
    try:
        result_filter = parse_query_params(request=request, query_class=MSResultFilter)
        mh = MSResultHandler()
        results, query_max_count = await mh.filter_results_display(result_filter=result_filter)
        ah = MSAthleteHandler()
        for result in results:
            athlete = await ah.find_athlete(MSAthleteFilter(uid=[result['MSAthlete']]))
            result['MSAthlete'] = f"{athlete.first_name} {athlete.last_name}"
            result['Class'] = class_formatter(athlete.graduation_year)[1]
        response = {
            'results': results,
            'query_max_count': query_max_count,
        }
        return response
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


# @router.put('/{result_id}', status_code=200)
# async def update_result(result_id: str, result: Result):
#     rh = MSResultHandler()
#     try:
#         updated_result = await rh.update_result(result_uid=result_id, result=result)
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
#     return updated_result


# @router.get('/{result_id}', status_code=200)
# async def find_result(result_id: str):
#     rh = MSResultHandler()
#     try:
#         result = await rh.find_result(result_uid=result_id)
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
#     return result


# @router.put('/{result_id}/activate', status_code=200)
# async def activate_result(result_id: str):
#     rh = MSResultHandler()
#     try:
#         updated_result = await rh.set_activation(result_uid=result_id, active_state=True)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_result


# @router.put('/{result_id}/deactivate', status_code=200)
# async def deactivate_result(result_id: str):
#     rh = MSResultHandler()
#     try:
#         updated_result = await rh.set_activation(result_uid=result_id, active_state=False)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_result


# @router.delete('/{result_id}', status_code=200)
# async def delete_result(result_id: str):
#     rh = MSResultHandler()
#     try:
#         updated_result = await rh.delete_result(result_uid=result_id)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_result
