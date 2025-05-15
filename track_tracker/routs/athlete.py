from re import L
from fastapi import APIRouter, HTTPException, Request, Response, Depends

# from models import MSAthlete, MSAthleteFilter
# # from handlers import MSAthleteHandler
from handlers import MSAthleteHandler, MSResultHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
# # from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import MSAthleteData, MSAthleteApiCreate, MSAthleteFilter, MSResultFilter, ContextSingleton, RestHeaders



context = ContextSingleton()

router = APIRouter(
    prefix='/athlete',
    tags=['athlete'],
)


@router.post('/', status_code=201)
async def create_athlete(athlete: MSAthleteApiCreate):
    try:
        existing_athlete_filter = MSAthleteFilter(first_name=[athlete.first_name], last_name=[athlete.last_name], team=[athlete.team])
        print(existing_athlete_filter)
        ah = MSAthleteHandler()
        existing_athlete = await ah.find_athlete(athlete_filter=existing_athlete_filter, silence_missing=True)
        if existing_athlete:
            # Verify the record doesnt already exist
            raise DuplicateRecordsException(f"first_name={athlete.first_name}, last_name={athlete.last_name}, team={athlete.team}")
        athlete_data = athlete.cast_data_object()
        created_athlete = await ah.create_athlete(athlete=athlete_data)
        return created_athlete.put
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/', status_code=200)
async def filter_athlete(request: Request):
    try:
        athlete_filter = parse_query_params(request=request, query_class=MSAthleteFilter)
        ah = MSAthleteHandler()
        athletes = await ah.filter_athletes(athlete_filter=athlete_filter)
        return {'athletes': athletes}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/{first}/{last}/{team}', status_code=200)
async def find_athlete(request: Request, first: str, last: str, team: str):
    try:
        athlete_filter = MSAthleteFilter(first_name=[first], last_name=[last], team=[team])
        ah = MSAthleteHandler()
        athlete = await ah.find_athlete(athlete_filter=athlete_filter)
        return athlete
    except MissingRecordException as err:
        message = f"No record found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=404, detail=message)
    except DuplicateRecordsException as err:
        message = f"Duplicate records found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=400, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.put('/', status_code=201)
async def update_athlete(athlete: MSAthleteData):
    try:
        ah = MSAthleteHandler()
        created_athlete = await ah.update_athlete(athlete=athlete)
        return created_athlete.put
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.delete('/{athlete_uid}', status_code=200)
async def find_athlete(request: Request, athlete_uid: str):
    try:
        ah = MSAthleteHandler()
        athlete = await ah.delete_athlete(athlete_uid=athlete_uid)
        return athlete
    except MissingRecordException as err:
        message = f"No record found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=404, detail=message)
    except DuplicateRecordsException as err:
        message = f"Duplicate records found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=400, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.get('/display', status_code=200)
async def filter_athlete(request: Request):
    try:
        athlete_filter = parse_query_params(request=request, query_class=MSAthleteFilter)
        ah = MSAthleteHandler()
        athletes, query_max_count = await ah.filter_athletes_display(athlete_filter=athlete_filter)
        mh = MSResultHandler()
        for athlete in athletes:
            results, _ = await mh.filter_results_display(MSResultFilter(athlete_uid=[athlete['uid']]))
            athlete_results = {}
            for result in results:
                event = result['Event']
                if event not in athlete_results:
                    athlete_results[event] = []
                athlete_results[event].append(result)
            athlete['results'] = athlete_results
        response = {
            'athletes': athletes,
            'query_max_count': query_max_count,
        }
        return response
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.get('/pr-graph', status_code=201)
async def generate_athlete_pr_graph(request: Request):
    athlete_filter = parse_query_params(request=request, query_class=MSAthleteFilter)
    ah = MSAthleteHandler()
    rh = MSResultHandler()
    athletes = await ah.filter_athletes(athlete_filter=athlete_filter)
    athlete_graph = [{'athlete': a} for a in athletes]
    # athlete_graph = [{'athlete': a} for a in athletes if 'Lil' in a.first_name]
    for graph_item in athlete_graph:
        athlete = graph_item['athlete']
        result_filter = MSResultFilter(athlete_uid=[athlete.uid], order_by=['meet_date'])
        results = await rh.filter_results(result_filter=result_filter)
        pr_data = {}
        for result in results:
            if result.event not in pr_data:
                result.result_metadata['PR'] = True
                pr_data[result.event] = result
            else:
                if result.result > pr_data[result.event].result:
                    result.result_metadata['PR'] = True
                    pr_data[result.event] = result
        graph_item['results'] = results
        graph_item['pr_data'] = pr_data


    return {'athletes_graph': athlete_graph}


    # try:
    #     athlete_filter = parse_query_params(request=request, query_class=MSAthleteFilter)
    #     ah = MSAthleteHandler()
    #     athletes = await ah.filter_athletes(athlete_filter=athlete_filter)
    #     return {'athletes': athletes}
    # except Exception as err:
    #     context.logger.warning(f'ERROR: {err}')
    #     raise HTTPException(status_code=500, detail='Internal Service Error')


# @router.put('/{athlete_id}', status_code=200)
# async def update_athlete(athlete_id: str, athlete: MSAthlete):
#     rh = MSAthleteHandler()
#     try:
#         updated_athlete = await rh.update_athlete(athlete_uid=athlete_id, athlete=athlete)
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
#     return updated_athlete


# @router.get('/{athlete_id}', status_code=200)
# async def find_athlete(athlete_id: str):
#     rh = MSAthleteHandler()
#     try:
#         athlete = await rh.find_athlete(athlete_uid=athlete_id)
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
#     return athlete


# @router.put('/{athlete_id}/activate', status_code=200)
# async def activate_athlete(athlete_id: str):
#     rh = MSAthleteHandler()
#     try:
#         updated_athlete = await rh.set_activation(athlete_uid=athlete_id, active_state=True)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_athlete


# @router.put('/{athlete_id}/deactivate', status_code=200)
# async def deactivate_athlete(athlete_id: str):
#     rh = MSAthleteHandler()
#     try:
#         updated_athlete = await rh.set_activation(athlete_uid=athlete_id, active_state=False)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_athlete


# @router.delete('/{athlete_id}', status_code=200)
# async def delete_athlete(athlete_id: str):
#     rh = MSAthleteHandler()
#     try:
#         updated_athlete = await rh.delete_athlete(athlete_uid=athlete_id)
#     # except MissingRecordException as err:
#     #     message = f"Record not found: [{err}]"
#     #     context.logger.warning(message)
#     #     raise HTTPException(status_code=404, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')
#     return updated_athlete
