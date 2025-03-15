import asyncio

from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import AthleteFilter, ResultFilter, ContextSingleton
from handlers import AthleteHandler, ResultHandler, parse_query_params, DuplicateRecordsException, MissingRecordException


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
    prefix='/record',
    tags=['record'],
)
'''HTML pages for viewing and filtering different results for school or state records.'''


@router.get('/')
async def html_record(request: Request):
    ah = AthleteHandler()
    mh = ResultHandler()
    offset = 0
    checking = True
    size = ResultFilter().limit
    results = []
    while checking:
        results_l = await mh.filter_results(ResultFilter(offset=offset))
        results.extend(results_l)
        if len(results_l) < size:
            checking = False
        offset += size
        await asyncio.sleep(0)

    # APPLY A FILTER TO ONLY GET ACTIVE TEAM MEMEBRS
    # DISPLAY HOW MANY STUDENTS ARE IN EACH GRADE?

    event_details = {}
    for result in results:
        if result.event not in event_details:
            athlete = await ah.find_athlete(AthleteFilter(uid=[result.athlete_uid]))
            result.athlete = athlete
            event_details[result.event] = result
        else:
            if result.result > event_details[result.event].result:
                # New record
                athlete = await ah.find_athlete(AthleteFilter(uid=[result.athlete_uid]))
                result.athlete = athlete
                event_details[result.event] = result
    record_page = await filter_records_html_page(event_details)
    return HTMLResponse(content=record_page, status_code=200)
