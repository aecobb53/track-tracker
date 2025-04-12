from datetime import date, datetime, timedelta
from multiprocessing.sharedctypes import Value
from tkinter import E
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

import os
import json
import yaml
import re
# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton
from models import MeetDay, Meet, Result
# from .html.unimplemented_page import unimplemented_page
from handlers import AthleteHandler, ResultHandler
from models import AthleteFilter, ResultFilter
from html import TEAM


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


def compare_results(event_str, old, new):
    """
    Return PR?, old_result, new_result
    """
    event_str = interpret_event(event_str)
    # print(f"    COMPARING OLD: {old}, NEW: {new} FOR EVENT: {event_str}")
    result_old = Result.parse_event_result(event=event_str, result=old)
    # print(f"    RESULT old: {result_old}")
    result_new = Result.parse_event_result(event=event_str, result=new)
    # print(f"    RESULT new: {result_new}")
    if result_new.is_none and result_old.is_none:
        return False, '-', '-'
    elif result_new > result_old:
        return True, result_old, result_new
    else:
        return False, result_old, result_new


def interpret_event(event):
    re_match_1_s = r'(\d ?[mM])$'
    re_match_2_s = r'(\d ?[mM] ?)'

    re_match_1 = re.search(re_match_1_s, event)
    re_match_2 = re.search(re_match_2_s, event)
    if re_match_1:
        event_l = [
            event[:re_match_1.start()+1],
            ' Meter',
            event[re_match_1.end():]]
        # print(f"OLD STRING: {event}")
        event = re.sub(r"\s+", ' ', ''.join(event_l)).strip()
        # print(f"NEW STRING: {event}")
    elif re_match_2:
        event_l = [
            event[:re_match_2.start()+1],
            ' Meter',
            event[re_match_2.end()-1:]]
        # print(f"OLD STRING: {event}")
        event = re.sub(r"\s+", ' ', ''.join(event_l)).strip()
        # print(f"NEW STRING: {event}")

    return event


def temp_function_compare_meet_data(local_meet_events, remote_meet_events, local_file_last_update_datetime, remote_file_last_update_datetime):
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
        remote_meet_events.pop(0)

        # print(f"local_meet_events: {len(local_meet_events)}")
        # print(f"remote_meet_events: {len(remote_meet_events)}")

        if len(local_meet_events) > len(remote_meet_events):
            # Local event needs to be removed
            for index, (local_event, remote_event) in enumerate(zip(local_meet_events, remote_meet_events)):
                if local_event['Event'] != remote_event['event'][0]:
                    local_meet_events.pop(index)
                    local_changed = True
                    break
        elif len(local_meet_events) < len(remote_meet_events):
            # Local needs to add an event
            for index, (local_event, remote_event) in enumerate(zip(local_meet_events, remote_meet_events)):
                if local_event['Event'] != remote_event['event'][0]:
                    new_event = {
                        'Event': remote_event['event'][0],
                        'Event Time': "-",
                        'athletes': [],
                    }
                    local_meet_events.insert(index, new_event)
                    break
            else:
                print('NO EVENT FOUND SO IT MUST BE THE LAST ONE')
            pass
        else:
            pass

        # print('FIXEDD')
        # print(f"local_meet_events: {len(local_meet_events)}")
        # print(f"remote_meet_events: {len(remote_meet_events)}")

        for index1, (local_event, remote_event) in enumerate(zip(local_meet_events, remote_meet_events)):
            print(f"INDEX: {index1}, LE: {local_event['Event']}, RE: {remote_event['event'][0]}")
            # print(f"LOCAL: {local_event}")
            # print(f"REMOTE: {remote_event}")
            # for a1 in local_event['athletes']:
            #     print(f"    LOCAL: {a1['name']}")
            # for a2 in remote_event['athletes']:
            #     print(f"    REMOTE: {a2}")
            if local_event.get('relay'):
                # print('NOT WORKING ON RELAYS YET!!!')
                pass
            else:
                tweaking = True
                rescue = 100
                while tweaking:
                    tweaking = False
                    if len(local_event['athletes']) != len(remote_event['athletes']):
                        print('investigating')
                        """
                        Since I only add one empty athlete column, it should be pretty easy to see which one was added
                        """
                        tweaking = True
                        # print(local_event['athletes'])
                        # print(remote_event['athletes'])
                        # for a1 in local_event['athletes']:
                        #     print(f"LOCAL: {a1['name']}")
                        # for a2 in remote_event['athletes']:
                        #     print(f"REMOTE: {a2}")
                        for index in range(max(len(local_event['athletes']), len(remote_event['athletes']))):
                            if len(local_event['athletes']) > len(remote_event['athletes']):
                                # Need to remove
                                local_event['athletes'].pop(index)
                                break
                            else:
                                if len(local_event['athletes']) and len(local_event['athletes']) > index:
                                    # There are at least some local athletes
                                    # if len(local_event['athletes']) < index:
                                    #     athlete_1 = None
                                    # else:
                                    #     athlete_1 = local_event['athletes'][index]['name']
                                    athlete_1 = local_event['athletes'][index]['name']
                                else:
                                    athlete_1 = None
                                print(f"THING: LEN {len(remote_event['athletes'])}, INDEX: {index}")
                                if len(remote_event['athletes']) and len(remote_event['athletes']) > index:
                                    # There are at least some remote athletes
                                    athlete_2 = remote_event['athletes'][index]
                                else:
                                    athlete_2 = None
                                
                                if not athlete_1 and not athlete_2:
                                    print('PROBLEM WHERE BOTH ATHLETES ARE NOT VALID')
                                    print(f"LOCAL: {local_event}")
                                    print(f"REMOTE: {remote_event}")
                                    print(f"LOCAL ATHLETE: {athlete_1}")
                                    print(f"REMOTE ATHLETE: {athlete_2}")
                                    raise ValueError('Both athletes are not valid')
                                elif athlete_1 != athlete_2:
                                    local_event['athletes'].insert(index, {'name': athlete_2})
                                    

                                # # Need to add
                                # # if len(remote_event['athletes']) + 1 < index:
                                # # print(local_event)
                                # # print(remote_event)
                                # # for a1 in local_event['athletes']:
                                # #     print(f"LOCAL: {a1['name']}")
                                # # for a2 in remote_event['athletes']:
                                # #     print(f"REMOTE: {a2}")
                                # if len(local_event['athletes']):
                                #     # There are at least some local athletes
                                #     if len(local_event['athletes']) < index:
                                #         athlete_1 = None
                                #     else:
                                #         athlete_1 = local_event['athletes'][index]['name']
                                #     athlete_2 = remote_event['athletes'][index]
                                #     if athlete_1 != athlete_2:
                                #         local_event['athletes'].insert(index, {'name': athlete_2})
                                #         break
                                # else:
                                #     # There are no local athletes
                                #     # for athlete_2 in remote_event['athletes'][index]
                                #     pass

                                
                                # print(f"INDEX AND LEN CHECK: len(local_event['athletes']): {len(local_event['athletes'])}, INDEX: {index}")
                                # if len(local_event['athletes']) < index:
                                #     athlete_1 = None
                                # else:
                                #     athlete_1 = local_event['athletes'][index]['name']
                                # athlete_2 = remote_event['athletes'][index]
                                # if athlete_1 != athlete_2:
                                #     local_event['athletes'].insert(index, {'name': athlete_2})
                                #     break
                    rescue -= 1
                    if rescue <= 0:
                        print(f"RESCUE TIMEOUT")
                        break

            if local_event['Event'] != remote_event['event'][0].strip():
                local_changed = True
                local_event['Event'] = remote_event['event'][0].strip()
            if local_event['Event Time'] != remote_event['time'][0].strip():
                local_changed = True
                local_event['Event Time'] = remote_event['time'][0].strip()
            for index2, (local_athlete, remote_athlete) in enumerate(zip(local_event.get('athletes', []), remote_event.get('athletes', []))):
                if local_athlete['name'] != remote_athlete.strip():
                    local_changed = True
                    local_athlete['name'] = remote_athlete.strip()
                    local_athlete['athlete_uid'] = None
                    local_athlete['seed_uid'] = None
                    local_athlete['result_uid'] = None
                    local_athlete['pr'] = None
            if local_event.get('relay'):
                local_teams = []
                remote_teams = [{
                    'name': None,
                    'athletes': [],
                }]
                for team in local_event.get('teams', []):
                    team_dict = {
                        'name': team.get('name'),
                        'athletes': [],
                    }
                    for athlete in team.get('athletes', []):
                        if athlete['name'].lower().startswith('team'):
                            continue
                        team_dict['athletes'].append(athlete['name'])
                    local_teams.append(team_dict)
                # remote_athlete_index_pointer = 0
                remote_team_pointer = 0
                remote_team_dict = {}
                for athlete in remote_event.get('athletes', []):
                    if athlete.lower().startswith('team'):
                        remote_team_pointer += 1
                        remote_team_dict = {
                            'name': athlete,
                            'athletes': [],
                        }
                        remote_teams.append(remote_team_dict)
                    else:
                        if not remote_teams:
                            remote_teams.append(remote_team_dict)
                        remote_teams[remote_team_pointer]['athletes'].append(athlete)
                for delete_index in reversed(range(len(remote_teams))):
                    if not remote_teams[delete_index]['name'] and not remote_teams[delete_index]['athletes']:
                        del remote_teams[delete_index]
                # print('')
                # print('HERE')
                # print(remote_teams)
                for local_team, remote_team in zip(local_teams, remote_teams):
                    # print(f"THING1: {local_team}")
                    # print(f"THING2: {remote_team}")
                    if local_team['name'] != remote_team['name']:
                        local_changed = True
                        local_team['name'] = remote_team['name']
                        # print(f'TEAM NAME CHANGED')
                    # if len(local_team['athletes']) != len(remote_team['athletes']):
                        # print(f"THE LENGTHS ARE DIFFERENT COME BACK TO BUILD THIS OUT")
                    for local_athlete, remote_athlete in zip(local_team['athletes'], remote_team['athletes']):
                        if local_athlete != remote_athlete:
                            local_changed = True
                            local_athlete = remote_athlete
                            # print(f'ATHLETE NAME CHANGED')

                # for index2, (local_athlete, remote_athlete) in enumerate(zip(local_event.get('athletes', []), remote_event.get('athletes', []))):
                #     # print(f"    ATHLETES: {local_athlete}, {remote_athlete}")
                #     if local_athlete['name'] != remote_athlete.strip():
                #         # print(f"    ATHLETES ARE DIFFERENT: {local_athlete}, {remote_athlete}")
                #         local_changed = True
                #         local_athlete['name'] = remote_athlete.strip()
                #         local_athlete['athlete_uid'] = None
                #         local_athlete['seed_uid'] = None
                #         local_athlete['result_uid'] = None
                #         local_athlete['pr'] = None
            for index2, (local_athlete, remote_athlete) in enumerate(zip(local_event.get('athletes', []), remote_event.get('heats', []))):
                if local_athlete.get('Heat/Lane/Flight') != remote_athlete.strip():
                    local_changed = True
                    local_athlete['Heat/Lane/Flight'] = remote_athlete.strip()
            for index2, (local_athlete, remote_athlete) in enumerate(zip(local_event.get('athletes', []), remote_event.get('seeds', []))):
                if local_athlete.get('seed') != remote_athlete.strip():
                    local_changed = True
                    local_athlete['seed'] = remote_athlete.strip()
                    local_athlete['seed_uid'] = None
                    local_athlete['pr'] = None
                    # FIND A WAY TO UPDATE THE PR IF THE SEED CHANGES AND IS NOW BELOW THE RESULT
            for index2, (local_athlete, remote_athlete) in enumerate(zip(local_event.get('athletes', []), remote_event.get('result', []))):
                if local_athlete.get('result') != remote_athlete.strip():
                    if not local_athlete.get('result') and not remote_athlete.strip():
                        continue
                    old = local_athlete['seed']
                    local_changed = True
                    local_athlete['result'] = remote_athlete.strip()
                    new = local_athlete['result']
                    pr, result_old, result_new = compare_results(local_event['Event'], old, new)
                    if pr:
                        local_athlete['pr'] = result_new.format
                    else:
                        local_athlete['pr'] = '-'
                    local_athlete['result_uid'] = None
                    local_meet_events[index1]['athletes'][index2] = local_athlete
            # for index2, (local_athlete, remote_athlete) in enumerate(zip(local_event.get('athletes', []), remote_event.get('place', []))):
            #     if local_athlete.get('place') != remote_athlete.strip():
            #         print('PLACE')
            #         local_changed = True
            #         local_athlete['place'] = remote_athlete.strip()

    else:
        print('INVALID UPDATE, skipping')

    current_meet = local_meet_events
    remote_updates = []
    return current_meet, remote_updates, local_changed, force_reload


@router.post('/')
async def post_meet(meet: Meet):
    for fl in os.listdir('/db/meets'):
        if fl == f"{meet.name}.json":
            with open(os.path.join('/db/meets', fl), 'r') as jf:
                meet_file_data = json.load(jf)
            break
    else:
        print(f"COULD NOT FIND MEET")

    local_file_last_update_datetime = datetime.strptime(meet_file_data['meet']['last_updated'], "%Y-%m-%d %H:%M:%S")
    if meet.data_time_version:
        remote_file_last_update_datetime = datetime.strptime(meet.data_time_version, "%Y-%m-%d %H:%M:%S")
    else:
        remote_file_last_update_datetime = None
    current_meet_events, remote_updates, local_changed, force_reload = temp_function_compare_meet_data(
        local_meet_events=meet_file_data['events'],
        remote_meet_events=meet.events,
        local_file_last_update_datetime=local_file_last_update_datetime,
        remote_file_last_update_datetime=remote_file_last_update_datetime)


    meet_data = meet_file_data['meet']
    event_data = []  # meet_file_data['events']
    meet_data_update = remote_updates

    # Populating with default seed, pr, etc data
    athlete_or_result_pulled = False
    """
    If athlete already pulled, dont find again. Assume its up to date
    Only pull result data that occured before the meet
    If there is an update to any row, pull all new records just in case
    Dont overwrite time/place, assume its just a name change and the rest should act accordingly
    """

    async def _format_athlete(athlete, meet, ah, rh, athlete_or_result_pulled):
        athlete['result'] = athlete.get('result', None)
        athlete['place'] = athlete.get('place', None)
        athlete['pr'] = athlete.get('pr', '-')
        athlete['points'] = athlete.get('points', '-')
        athlete['athlete_uid'] = athlete.get('athlete_uid', None)
        athlete['seed_uid'] = athlete.get('seed_uid', None)
        athlete['result_uid'] = athlete.get('result_uid', None)
        if not athlete.get('Heat/Lane/Flight'):
            athlete['Heat/Lane/Flight'] = '-'
        seed = athlete.get('seed', '-')

        # Pull athlete data
        if not athlete.get('athlete_uid') or meet.run_full_update:
            first_last = athlete['name'].split(' ')
            first = first_last.pop(0)
            last = ' '.join(first_last)
            af = AthleteFilter(
                first_name=[first],
                last_name=[last],
                team=[TEAM],
            )
            athlete_obj = await ah.find_athlete(af, silence_missing=True, silence_dupe=True)
            event_search_name = interpret_event(event['Event'])

            if athlete_obj:
                athlete_or_result_pulled = True
                athlete['athlete_uid'] = athlete_obj.uid
                rf_pr = ResultFilter(
                    athlete_uid=[athlete_obj.uid],
                    team=[TEAM],
                    event=[event_search_name],
                    meet_date=[f"Before{datetime.strftime(meet_date - timedelta(days=1), '%Y-%m-%d')}"]
                )
                results_pr = await rh.filter_results(rf_pr)
                if results_pr:
                    pr = results_pr[0]
                    for result in results_pr:
                        if result.result > pr.result:
                            pr = result
                else:
                    pr = None
                if pr:
                    seed = pr.result.format
                    athlete_or_result_pulled = True
                    athlete['seed_uid'] = pr.uid

        athlete['seed'] = seed
        return athlete_or_result_pulled

    meet_date = datetime.strptime(meet_file_data['meet']['date'], "%Y-%m-%d")
    ah = AthleteHandler()
    rh = ResultHandler()
    for event in current_meet_events:
        event_dict = {
            'time': event['Event Time'],
            'event': event['Event'],
        }
        athletes = []
        for athlete in event.get('athletes', []):
            athlete_or_result_pulled = await _format_athlete(athlete, meet, ah, rh, athlete_or_result_pulled)
            athletes.append(athlete)

        for team in event.get('teams', []):
            # This is such a shitty hack. I am angry with myself. But just need it working for now
            for index in reversed(range(len(team.get('athletes', [])))):
                # This is a hack to remove the team name from the athletes list since I add them in a sec for display purposes
                row = team['athletes'][index]
                if row['name'].startswith('Team'):
                    team['athletes'].pop(index)
            if team.get('name'):
                team['athletes'].insert(0, {
                    'name': team['name'],
                    'Heat/Lane/Flight': team.get('Heat/Lane/Flight'),
                })
            for athlete in team.get('athletes', []):
                athlete_or_result_pulled = await _format_athlete(
                    athlete,
                    meet,
                    ah,
                    rh,
                    athlete_or_result_pulled)
                athletes.append(athlete)

        event_dict['athletes'] = athletes
        event_data.append(event_dict)

    if local_changed or meet.run_full_update:
        for event in event_data:
            event_search_name = interpret_event(event['event'])
            for athlete in event.get('athletes', []):
                seed = athlete.get('seed', '')
                if seed == '-':
                    seed = None
                result = athlete.get('result', '')
                if result == '-':
                    result = ''

                if not athlete.get('athlete_uid'):
                    first_last = athlete['name'].split(' ')
                    first = first_last.pop(0)
                    last = ' '.join(first_last)
                    af = AthleteFilter(
                        first_name=[first],
                        last_name=[last],
                        team=[TEAM],
                    )
                    athlete_obj = await ah.find_athlete(af, silence_missing=True, silence_dupe=True)
                    if athlete_obj:
                        athlete['athlete_uid'] = athlete_obj.uid

                if ( not result or meet.run_full_update ) and athlete['athlete_uid']:
                    # LOOK FOR NEW RESULTS

                    rf_pr = ResultFilter(
                        athlete_uid=[athlete['athlete_uid']],
                        event=[event_search_name],
                        meet_date=[
                            f"After{datetime.strftime(meet_date - timedelta(days=1), '%Y-%m-%d')}",
                            f"Before{datetime.strftime(meet_date + timedelta(days=1), '%Y-%m-%d')}"
                            ]
                    )
                    results_pr = await rh.filter_results(rf_pr)
                    if results_pr:
                        for result_i in results_pr:
                            athlete['result'] = result_i.result.format
                            athlete['result_uid'] = result_i.uid
                            athlete_or_result_pulled = True
                            result = result_i.result.format
                if result:
                    if seed:
                        new_pr, _, result_new = compare_results(event_str=event_search_name, old=seed, new=result)
                        if new_pr:
                            athlete['pr'] = result_new.format
                    else:
                        athlete['pr'] = result

    if local_changed or athlete_or_result_pulled:
        # SAVE NEW VERSION
        meet_file_data['events'] = current_meet_events
        meet_file_data['meet']['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(os.path.join('/db/meets', fl), 'w') as jf:
            jf.write(json.dumps(meet_file_data, indent=4))

    output = {
        'data_timestamp': meet_file_data['meet']['last_updated'],
        'meet_data': meet_data,
        'event_header': [
            {'name': 'Time', 'class': 'col-width-time'},
            {'name': 'Event', 'class': 'col-width-event'},
            {'name': 'Athlete', 'class': 'col-width-athlete'},
            {'name': 'Heat/Lane/Flight', 'class': 'col-width-heat'},
            {'name': 'Seed', 'class': 'col-width-seed'},
            {'name': 'Result', 'class': 'col-width-result'},
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
