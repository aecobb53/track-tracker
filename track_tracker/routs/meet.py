import os
from fastapi import APIRouter, HTTPException, Request, Response, Depends

# from models import MSAthlete, MSAthleteFilter
# # from handlers import MeetHandler
from handlers import MeetHandler, parse_query_params, DuplicateRecordsException, MissingRecordException
# # from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import MSAthleteData, MSAthleteApiCreate, MSAthleteFilter, MSResultFilter, ContextSingleton, RestHeaders, MeetEvent, Meet, MeetApiCreate, MeetEventAthlete, MeetEventAthleteAPICreate



context = ContextSingleton()

router = APIRouter(
    prefix='/meet',
    tags=['meet'],
)


# @router.post('/', status_code=201)
# async def create_athlete(athlete: MSAthleteApiCreate):
#     try:
#         existing_athlete_filter = MSAthleteFilter(first_name=[athlete.first_name], last_name=[athlete.last_name], team=[athlete.team])
#         print(existing_athlete_filter)
#         mh = MeetHandler()
#         existing_athlete = await ah.find_athlete(athlete_filter=existing_athlete_filter, silence_missing=True)
#         if existing_athlete:
#             # Verify the record doesnt already exist
#             raise DuplicateRecordsException(f"first_name={athlete.first_name}, last_name={athlete.last_name}, team={athlete.team}")
#         athlete_data = athlete.cast_data_object()
#         created_athlete = await ah.create_athlete(athlete=athlete_data)
#         return created_athlete.put
#     except DuplicateRecordsException as err:
#         message = f"Dupe record attempt: {err}"
#         context.logger.warning(message)
#         raise HTTPException(status_code=409, detail=message)
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')

@router.post('/{meet_name}', status_code=201)
async def create_meet(meet_name: str, meet_create: MeetApiCreate, request: Request):
    meet = meet_create.cast_data_object()
    try:
        events_forming = []
        events_forming += ['Long Jump', 'Triple Jump', 'High Jump', 'Pole Vault']
        events_forming += ['Shot Put', 'Discus']
        events_forming += ['4x800', '100 H', '100m', '4x200', '1600m', '4x100', '400m', '300 H', '800m', '200m', '3200m', '4x400']
        events = []
        for event in events_forming:
            if event == '100 H':
                events.append(f"Girls {event}")
                event = event.replace('100', '110')
                events.append(f"Boys {event}")
            else:
                events.append(f"Girls {event}")
                events.append(f"Boys {event}")
        print(f"MEET CREATE: {meet_create}")
        if meet_create.auto_populate_events:
            meet.events = [MeetEvent(event_name=e) for e in events]

        mh = MeetHandler(meet_name=meet_name, skip_load=True)
        mh.content = meet
        mh.save_file()
        return mh.content
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.get('/', status_code=200)
async def filter_meet(request: Request):
    try:
        meet_names = []
        if os.path.exists('/db/meet'):
            for fl in os.listdir('/db/meet'):
                if fl.startswith('meet_') and fl.endswith('.json'):
                    meet_names.append(fl[5:-5])
        else:
            meet_names = []
        return {'meet_names': meet_names}
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.get('/{meet_name}', status_code=200)
async def find_meet(meet_name: str, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        return mh.content
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')


@router.delete('/{meet_name}', status_code=200)
async def delete_meet(meet_name: str, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name, skip_load=True)
        try:
            mh.load_file()
            output = mh.content
        except Exception as err:
            context.logger.warning(f'ERROR: {err}')
            output = None
        mh.move_file(new_directory='meet/deleted')
        if output:
            return output
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')



@router.post('/{meet_name}/{event_name}', status_code=201)
async def create_meet_event(meet_name: str, event_name: str, event: MeetEvent, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.add_event(event=event)
        mh.save_file()
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

# @router.get('/{meet_name}', status_code=200)
# async def filter_meet_events(meet_name: str, request: Request):
#     try:
#         mh = MeetHandler(meet_name=meet_name)
#         mh.load_file()
#         for event in mh.content.events:
#             if 
#         return mh.content
#     except Exception as err:
#         context.logger.warning(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Service Error')

@router.get('/{meet_name}/{event_name}', status_code=200)
async def find_meet_event(meet_name: str, event_name: str, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        meet_event, _ = mh.find_event(event_name=event_name)
        return meet_event
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.put('/{meet_name}/{event_name}', status_code=200)
async def update_meet_event(meet_name: str, event_name: str, event: MeetEvent, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        mh.update_event(event_name=event_name, event=event)
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.put('/{meet_name}/{event_name}/{index}', status_code=200)
async def reorder_meet_events(meet_name: str, event_name: str, index: int, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        mh.move_event(new_event_index=index, event_name=event_name)
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.delete('/{meet_name}/{event_name}', status_code=200)
async def delete_meet_event(meet_name: str, event_name: str, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.delete_event(event_name=event_name)
        mh.save_file()
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')



@router.post('/{meet_name}/{event_name}/athlete', status_code=201)
async def create_meet_event_athlete(meet_name: str, event_name: str, athlete_create: MeetEventAthleteAPICreate, request: Request):
    try:
        athlete = athlete_create.cast_data_object()
        mh = MeetHandler(meet_name=meet_name)
        mh.add_event_athlete(event_name=event_name, athlete=athlete)
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

# # @router.get('/{meet_name}', status_code=200)
# # async def filter_meet_events_athlete(meet_name: str, request: Request):

@router.get('/{meet_name}/{event_name}/athlete/{first}/{last}', status_code=200)
async def find_meet_event_athlete(meet_name: str, event_name: str, first: str, last: str, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        athlete, _ = mh.find_event_athlete(event_name=event_name, first=first, last=last)
        return athlete
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.get('/{meet_name}/athlete/{first}/{last}/{team}', status_code=200)
async def find_meet_athlete(meet_name: str, first: str, last: str, team: str, request: Request):
    try:
        athlete = {
            'first_name': first,
            'last_name': last,
            'team': team,
            'points': 0,
            'meets': [],
        }
        if os.path.exists('/db/meet'):
            for fl in os.listdir('/db/meet'):
                if fl.startswith('meet_') and fl.endswith('.json'):
                    meet_name = fl[5:-5]
                    meet = MeetHandler(meet_name=meet_name)
                    meet.load_file()
                    events = meet.find_athlete(first=first, last=last, team=team)
                    points = sum([e['athlete'].points for e in events if e['athlete'].points])
                    athlete['meets'].append({
                        'meet_name': meet_name,
                        'points': points,
                        'events': events
                    })
                    athlete['points'] += points
        return athlete
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')





@router.put('/{meet_name}/{event_name}/athlete/{first}/{last}', status_code=200)
async def update_meet_event_athlete(meet_name: str, event_name: str, first: str, last: str, athlete: MeetEventAthlete, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        mh.update_event_athlete(event_name=event_name, first=first, last=last, athlete=athlete)
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')

@router.delete('/{meet_name}/{event_name}/athlete/{first}/{last}', status_code=200)
async def delete_meet_event_athlete(meet_name: str, event_name: str, first: str, last: str, request: Request):
    try:
        mh = MeetHandler(meet_name=meet_name)
        mh.load_file()
        mh.delete_event_athlete(event_name=event_name, first=first, last=last)
    except MissingRecordException as err:
        message = f"Missing record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
