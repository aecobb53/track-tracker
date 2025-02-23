import asyncio

from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import AthleteFilter, MarkFilter, ContextSingleton
from handlers import AthleteHandler, MarkHandler, parse_query_params, DuplicateRecordsException, MissingRecordException


from html import (
    # create_record_html_page,
    # filter_records_html_page,
    # find_record_html_page,
    # record_base_page,
    filter_records_html_page,
    unimplemented_page,
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/record',
    tags=['record', 'html'],
)
'''HTML pages for viewing and filtering different results for school or state records.'''


@router.get('/')
async def html_record(request: Request):
    ah = AthleteHandler()
    mh = MarkHandler()
    offset = 0
    checking = True
    size = MarkFilter().limit
    marks = []
    while checking:
        marks_l = await mh.filter_marks(MarkFilter(offset=offset))
        marks.extend(marks_l)
        if len(marks_l) < size:
            checking = False
        offset += size
        await asyncio.sleep(0)

    # APPLY A FILTER TO ONLY GET ACTIVE TEAM MEMEBRS
    # DISPLAY HOW MANY STUDENTS ARE IN EACH GRADE?

    event_details = {}
    for mark in marks:
        if mark.event not in event_details:
            athlete = await ah.find_athlete(AthleteFilter(uid=[mark.athlete_uid]))
            mark.athlete = athlete
            event_details[mark.event] = mark
        else:
            if mark.mark > event_details[mark.event].mark:
                # New record
                athlete = await ah.find_athlete(AthleteFilter(uid=[mark.athlete_uid]))
                mark.athlete = athlete
                event_details[mark.event] = mark
    record_page = await filter_records_html_page(event_details)
    return HTMLResponse(content=record_page, status_code=200)
