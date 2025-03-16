from calendar import month
from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

import os
# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton
from models import MeetDay
# from .html.unimplemented_page import unimplemented_page
from handlers import WorkoutHandler, AthleteHandler
from models import WorkoutFilter, AthleteFilter


from html import (
    # create_meetday_html_page,
    # filter_meetdays_html_page,
    # find_meetday_html_page,
    # meetday_base_page,
    # filter_meetdays_html_page,
    # filter_meetdays_html_page,
    filter_meetdays_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/meetday',
    tags=['meetday'],
)


@router.post('/')
async def get_meetday(meetday: MeetDay):
# async def update_meetday():
    print(f'IN GET')
    # print(os.listdir('/'))
    date = '03-05'
    name = '4x400 Meter Repeats'
    with open(f"/db/{date}={name}.csv", 'r') as cf:
        local_csv = [[ll.strip() for ll in l.split(';')] for l in cf.readlines() if l]
    remote_csv = meetday.csv
    local_csv_update_string = []
    remote_csv_update_string = []

    if meetday.csv:
        for index_i in range(len(local_csv)):
            local_row = local_csv[index_i]
            # old_row = csv[index_i]
            if index_i < len(meetday.csv):
                remote_row = meetday.csv[index_i]
            else:
                local_csv_update_string.append(f"remove row [{index_i}]")
                continue
            
            for index_j in range(len(local_row)):
            

                """
                Removed rows in remote
                Removed rows in local
                New rows in remote
                New rows in local
                Changed data in remote
                Changed dat in local
                Add a timestamp of last update to know if things are allowed to be  updated
                """


    output = {
        'csv': csv,
        'csv_update': csv_update,
    }
    return output


# @router.post('/')
# async def update_meetday(meetday: MeetDay):
#     # mh = WorkoutHandler()
#     # meetdays = await mh.filter_meetdays(meetday_filter=WorkoutFilter())
#     # ah = AthleteHandler()
#     # for meetday in meetdays:
#     #     athlete = await ah.find_athlete(AthleteFilter(uid=[meetday.athlete_uid]))
#     #     meetday.athlete = athlete
#     # meetday_page = await filter_meetdays_html_page(meetdays=meetdays)
#     meetday_page = await filter_meetdays_html_page()
#     return HTMLResponse(content=meetday_page, status_code=200)
