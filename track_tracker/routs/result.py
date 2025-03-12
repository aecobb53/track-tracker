from fastapi import APIRouter, HTTPException, Request, Response, Depends

# from models import Result, ResultFilter
# # from handlers import ResultHandler
from handlers import AthleteHandler, ResultHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
# # from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
# from models import ResultData, ResultApiCreate, ResultFilter
from models import ResultData, ResultApiCreate, ResultFilter, AthleteFilter
from models import ContextSingleton

from typing import Annotated
from html.common import class_formatter

context = ContextSingleton()

router = APIRouter(
    prefix='/result',
    tags=['result'],
)


@router.post('/', status_code=201)
async def create_result(result: ResultApiCreate):
    try:
        ah = AthleteHandler()
        athlete = await ah.find_athlete(AthleteFilter(
            first_name=[result.athlete_first_name],
            last_name=[result.athlete_last_name],
            team=[result.team],
        ))
        result.athlete = athlete
        result_data = result.cast_data_object()
        mh = ResultHandler()

        existing_result_filter = ResultFilter(
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
        result_filter = parse_query_params(request=request, query_class=ResultFilter)
        ah = AthleteHandler()
        if result_filter.first_name or result_filter.last_name and not result_filter.athlete_uid:
            athlete_filter = AthleteFilter(
                first_name=result_filter.first_name,
                last_name=result_filter.last_name,
            )
            athlete = await ah.find_athlete(athlete_filter, silence_missing=True)
            if athlete:
                result_filter.athlete_uid = [athlete.uid]
        mh = ResultHandler()
        results = await mh.filter_results(result_filter=result_filter)
        for result in results:
            athlete = await ah.find_athlete(AthleteFilter(uid=[result.athlete_uid]))
            result.athlete = athlete
        return {'results': results}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.put('/', status_code=200)
async def update_result(result: ResultData):
    try:
        mh = AthleteHandler()
        created_result = await mh.update_result(result=result)
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
        result_filter = parse_query_params(request=request, query_class=ResultFilter)
        mh = ResultHandler()
        results, query_max_count = await mh.filter_results_display(result_filter=result_filter)
        ah = AthleteHandler()
        for result in results:
            athlete = await ah.find_athlete(AthleteFilter(uid=[result['Athlete']]))
            result['Athlete'] = f"{athlete.first_name} {athlete.last_name}"
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
#     rh = ResultHandler()
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
#     rh = ResultHandler()
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
#     rh = ResultHandler()
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
#     rh = ResultHandler()
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
#     rh = ResultHandler()
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
