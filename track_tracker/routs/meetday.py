from calendar import month
from datetime import date, datetime, timedelta
from threading import local
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

import os
import json
import yaml
# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton
from models import MeetDay, Meet
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


def temp_function_compare_meet_data(local_meet_events, remote_meet_events, local_file_last_update_datetime, remote_file_last_update_datetime):
    x=1
    print(f"LOCAL TIME: {local_file_last_update_datetime}")
    print(f"REMOTE TIME: {remote_file_last_update_datetime}")
    local_changed = False
    force_reload = False
    if remote_meet_events and remote_file_last_update_datetime:
        if local_file_last_update_datetime > remote_file_last_update_datetime:
            force_reload = True
            current_meet = local_meet_events
            remote_updates = []
            return current_meet, remote_updates, local_changed, force_reload
        # # CURRENTLY ASSUME EXACT SAME SIZE
        # VALIDATE THE TIMESTAMP OF THE DATA FROM REMOTE IS EQUAL TO THE DATA LAST UPDATED OR ELSE THERE IS MISSING DATA FOR REMOTE
        # EVENTUALLY ALLOW TIME AND EVENT UPDATES
        """
        Cases need to handle
        local and remote have no changes
        local is behind remote so local needs to update
        local is ahead of remote so remote needs to update
        local and remote are ahead of each other in different ways and both need to be updated
        local and remote have different athletes that conflict and remote needs to reset to local
        """
    
        for local_event, remote_event in zip(local_meet_events, remote_meet_events):
            if local_event['Event'] != remote_event['event'][0]:
                local_changed = True
                local_event['Event'] = remote_event['event'][0]
            if local_event['Event Time'] != remote_event['time'][0]:
                local_changed = True
                local_event['Event Time'] = remote_event['time'][0]
            for local_athlete, remote_athlete in zip(local_event.get('athletes', []), remote_event.get('athletes', [])):
                if local_athlete['name'] != remote_athlete:
                    local_changed = True
                    local_athlete['name'] = remote_athlete
            for local_athlete, remote_athlete in zip(local_event.get('athletes', []), remote_event.get('heats', [])):
                if local_athlete['Heat/Lane/Flight'] != remote_athlete:
                    local_changed = True
                    local_athlete['Heat/Lane/Flight'] = remote_athlete
            for local_athlete, remote_athlete in zip(local_event.get('athletes', []), remote_event.get('seeds', [])):
                if local_athlete['seed'] != remote_athlete:
                    local_changed = True
                    local_athlete['seed'] = remote_athlete
            for local_athlete, remote_athlete in zip(local_event.get('athletes', []), remote_event.get('result', [])):
                if local_athlete.get('result') != remote_athlete:
                    local_changed = True
                    local_athlete['result'] = remote_athlete
            for local_athlete, remote_athlete in zip(local_event.get('athletes', []), remote_event.get('place', [])):
                if local_athlete.get('place') != remote_athlete:
                    local_changed = True
                    local_athlete['place'] = remote_athlete
    else:
        print('INVALID UPDATE, skipping')

    current_meet = local_meet_events
    remote_updates = []
    return current_meet, remote_updates, local_changed, force_reload


@router.post('/')
async def get_meet(meet: Meet):
    print(f'IN GET')
    for fl in os.listdir('/db/meets'):
        if fl == f"{meet.name}.json":
            with open(os.path.join('/db/meets', fl), 'r') as jf:
                meet_file_data = json.load(jf)

    local_file_last_update_datetime = datetime.strptime(meet_file_data['meet']['last_updated'], "%Y-%m-%d %H:%M:%S")
    if meet.data_time_version:
        remote_file_last_update_datetime = datetime.strptime(meet.data_time_version, "%Y-%m-%d %H:%M:%S")
    else:
        remote_file_last_update_datetime = None
    current_meet_events, remote_updates, local_changed, force_reload = temp_function_compare_meet_data(
        local_meet_events=meet_file_data['events'], remote_meet_events=meet.events,
        local_file_last_update_datetime=local_file_last_update_datetime, remote_file_last_update_datetime=remote_file_last_update_datetime)
    if local_changed:
        # SAVE NEW VERSION
        print('SAVING NEW VERSION')
        meet_file_data['events'] = current_meet_events
        meet_file_data['meet']['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # with open(os.path.join('/db/meets', fl), 'w') as jf:
        #     jf.write(json.dumps(meet_file_data, indent=4))


    meet_data = meet_file_data['meet']
    event_data = []  # meet_file_data['events']
    meet_data_update = remote_updates
    for event in current_meet_events:
        event_dict = {
            'time': event['Event Time'],
            'event': event['Event'],
        }
        # print(f"EVENT: {event}")
        athletes = []
        for athlete in event.get('athletes', []):
            athlete['time/mark'] = None
            athlete['place'] = None
            athlete['pr'] = '-'
            athlete['points'] = '-'
            athletes.append(athlete)
        for team in event.get('teams', []):
            x=1
        event_dict['athletes'] = athletes
        # print(f"EVENT DICT: {event_dict}")
        event_data.append(event_dict)

    output = {
        'data_timestamp': meet_file_data['meet']['last_updated'],
        'meet_data': meet_data,
        'event_header': [
            {'name': 'Time', 'class': 'col-width-time'},
            {'name': 'Event', 'class': 'col-width-event'},
            {'name': 'Athlete', 'class': 'col-width-athlete'},
            {'name': 'Heat/Lane/Flight', 'class': 'col-width-heat'},
            {'name': 'Seed Time/Mark', 'class': 'col-width-seed'},
            {'name': 'Time/Mark', 'class': 'col-width-result'},
            {'name': 'Place', 'class': 'col-width-place'},
            {'name': 'New PR', 'class': 'col-width-pr'},
            {'name': 'Points', 'class': 'col-width-points'},
            ],
        'event_data': event_data,
        'meet_data_update': meet_data_update,
        'force_reload': force_reload,
    }
    return output



# @router.post('/')
# async def get_meet(meet: Meet):
# # async def update_meetday():
#     print(f'IN GET')
#     # print(os.listdir('/db/meets'))
#     # print(f"MEET: {meet}")
#     for fl in os.listdir('/db/meets'):
#         # print(f"MEET FL: {fl}")
#         if fl == f"{meet.name}.json":
#             with open(os.path.join('/db/meets', fl), 'r') as jf:
#                 meet_data = json.load(jf)
#     csv = []
#     csv_update = []
#     print(meet_data)
#     # date = '03-05'
#     # name = '4x400 Meter Repeats'
#     # with open(f"/db/{date}={name}.csv", 'r') as cf:
#     #     local_csv = [[ll.strip() for ll in l.split(';')] for l in cf.readlines() if l]
#     # remote_csv = meetday.csv
#     # local_csv_update_string = []
#     # remote_csv_update_string = []

#     # if meetday.csv:
#     #     for index_i in range(len(local_csv)):
#     #         local_row = local_csv[index_i]
#     #         # old_row = csv[index_i]
#     #         if index_i < len(meetday.csv):
#     #             remote_row = meetday.csv[index_i]
#     #         else:
#     #             local_csv_update_string.append(f"remove row [{index_i}]")
#     #             continue
            
#     #         for index_j in range(len(local_row)):
            

#     #             """
#     #             Removed rows in remote
#     #             Removed rows in local
#     #             New rows in remote
#     #             New rows in local
#     #             Changed data in remote
#     #             Changed dat in local
#     #             Add a timestamp of last update to know if things are allowed to be  updated
#     #             """


#     output = {
#         'csv': csv,
#         'csv_update': csv_update,
#     }
#     return output


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
