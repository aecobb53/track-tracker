import os
import json
from datetime import date, datetime, timedelta
import re
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton
# from .html.unimplemented_page import unimplemented_page
from handlers import ResultHandler, AthleteHandler
from models import ResultFilter, AthleteFilter
from html import TEAM



from html import (
    # create_meetday_html_page,
    # filter_meetdays_html_page,
    # find_meetday_html_page,
    # meetday_base_page,
    # filter_meetdays_html_page,
    # filter_meetdays_html_page,
    find_meet_html_page,
    filter_meetdays_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/meetday',
    tags=['meetday'],
)


# @router.get('/')
# async def html_meetday(request: Request):
#     # mh = WorkoutHandler()
#     # meetdays = await mh.filter_meetdays(meetday_filter=WorkoutFilter())
#     # ah = AthleteHandler()
#     # for meetday in meetdays:
#     #     athlete = await ah.find_athlete(AthleteFilter(uid=[meetday.athlete_uid]))
#     #     meetday.athlete = athlete
#     # meetday_page = await filter_meetdays_html_page(meetdays=meetdays)
#     meetday_page = await find_meet_html_page()
#     return HTMLResponse(content=meetday_page, status_code=200)


@router.get('/')
async def html_meetday(request: Request):
    print(f'MEETS PAGE')
    meets_dict = {}
    for fl in os.listdir('/db/meets'):
        if not fl.endswith('.json'):
            continue
        with open(os.path.join('/db/meets', fl), 'r') as jf:
            meet_file_data = json.load(jf)
            meet_metadata = meet_file_data['meet']
            print(f'MEET: {meet_metadata}')
            meets_dict[meet_metadata['meet_name']] = {
                'meet_date': datetime.strptime(meet_metadata['date'], '%Y-%m-%d'),
                'endpoint': f"meetday/{fl.replace('.json', '')}",
                'jv': meet_metadata.get('jv'),
            }

    meets_dict = dict(sorted(meets_dict.items(), key=lambda item: item[1]['meet_date'], reverse=False))
    meetday_page = await filter_meetdays_html_page(meets_dict=meets_dict)
    return HTMLResponse(content=meetday_page, status_code=200)


@router.get('/{meet_name}')
async def html_meetday(meet_name: str, request: Request):
    print(f'PAGE MEET: {meet_name}')
    # mh = WorkoutHandler()
    # meetdays = await mh.filter_meetdays(meetday_filter=WorkoutFilter())
    # ah = AthleteHandler()
    # for meetday in meetdays:
    #     athlete = await ah.find_athlete(AthleteFilter(uid=[meetday.athlete_uid]))
    #     meetday.athlete = athlete
    # meetday_page = await filter_meetdays_html_page(meetdays=meetdays)
    meetday_page = await find_meet_html_page(meet_name)
    return HTMLResponse(content=meetday_page, status_code=200)


# @router.get('/')
# async def html_meetday(request: Request):
#     # mh = WorkoutHandler()
#     # meetdays = await mh.filter_meetdays(meetday_filter=WorkoutFilter())
#     # ah = AthleteHandler()
#     # for meetday in meetdays:
#     #     athlete = await ah.find_athlete(AthleteFilter(uid=[meetday.athlete_uid]))
#     #     meetday.athlete = athlete
#     # meetday_page = await filter_meetdays_html_page(meetdays=meetdays)
#     meetday_page = await filter_meetdays_html_page()
#     return HTMLResponse(content=meetday_page, status_code=200)
