import os
import json
import requests
from datetime import datetime, timezone


etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
BIG_ASS_JSON_PATH = os.path.join(etc_tmp, 'upload_file.json')
SERVER_URL = 'http://localhost:8205'
CURRENT_YEAR = 2025

YEAR_MAP = {
    9: 'Freshman',
    10: 'Sophomore',
    11: 'Junior',
    12: 'Senior',
}


with open(BIG_ASS_JSON_PATH, 'r') as jf:
    data = json.load(jf)
x=1
for year, meets in data.items():
    for meet_name, events in meets.items():
        for event_name, results in events.items():
            for result in results:
                athlete = result.get('athlete')
                mark = result['mark']
                if athlete:
                    first = athlete['first_name']
                    last = athlete['last_name']
                    team = athlete['team']
                    athlete_resp = requests.get(f"{SERVER_URL}/athlete/{first}/{last}/{team}")
                    if athlete_resp.status_code == 404:
                        # Post new athlete
                        athlete_resp = requests.post(f"{SERVER_URL}/athlete", json=athlete)
                        if not athlete_resp.ok:
                            x=1
                    elif athlete_resp.ok:
                        # Compare the athlete data
                        athlete_content = athlete_resp.json()
                        update = False
                        for key, value in athlete.items():
                            if athlete_content[key] != value:
                                print('')
                                print('compared athletes but are different')
                                print(athlete_content)
                                print(athlete)
                                update = True
                                athlete_content[key] = value
                                x=1
                        if update:
                            x=1
                            athlete_resp = requests.put(f"{SERVER_URL}/athlete", json=athlete_content)
                            if not athlete_resp.ok:
                                x=1
                            x=1

                    else:
                        x=1
                    athlete_content = athlete_resp.json()
                    athlete_uid = athlete_content['uid']
                    mark['athlete_uid'] = athlete_uid
                    mark['athlete_first_name'] = first
                    mark['athlete_last_name'] = last
                    x=1
                else:
                    # No athlete (Relay)
                    x=1
                mark_resp = requests.post(f"{SERVER_URL}/mark", json=mark)
                mark_content = mark_resp.json()
                if not mark_resp.ok and mark_resp.status_code != 409:
                    x=1
                x=1
    x=1
x=1





# for meet, events in data.items():
#     # first_last = name.split(' ')
#     # first = first_last[0]
#     # last = ' '.join(first_last[1:])

#     # if first != 'Jackson' or last != 'Bates':
#     #     continue

#     for event_name, results in events.items():
#         for result in results:
#             if not result['meet_metadata']:
#                 # This is a JV meet or something that doesnt have any results
#                 continue
#             if not result.get('athlete'):
#                 # This is a relay
#                 continue
#             first_last = result['athlete'].split(' ')
#             first = first_last[0]
#             last = ' '.join(first_last[1:])

#             month, day = result['meet_metadata']['date'].split('/')
#             meet_date = datetime(result['calendar_year'], int(month), int(day))
#             meet_date = datetime.strftime(meet_date, '%Y-%m-%d')
#             meet = result['meet_metadata']['meet_name']

#             athlete_resp = requests.get(f"{SERVER_URL}/athlete/{first}/{last}/{result['team']}")
#             athlete_content = athlete_resp.json()
#             if athlete_resp.status_code == 404:
#                 # Need to add
#                 if 'year' in result:
#                     graduation_year = calculate_graduation_year(
#                         athlete_year=result['year'],
#                         event_year=result['calendar_year'])
#                 else:
#                     graduation_year = None
#                 athlete_post_body = {
#                     'first_name': first,
#                     'last_name': last,
#                     'team': result['team'],
#                     'graduation_year': graduation_year,
#                     'gender': None,
#                 }
#                 athlete_resp = requests.post(f"{SERVER_URL}/athlete", json=athlete_post_body)
#                 athlete_content = athlete_resp.json()
#             if 'uid' in athlete_content:
#                 athlete_uid = athlete_content['uid']
#             else:
#                 athlete_uid = None
#             mark_post_body = {
#                 'event': event_name,
#                 'heat': result['heat'],
#                 'place': result['place'],
#                 'wind': result['wind'],
#                 'athlete_uid': athlete_uid,
#                 'athlete_first_name': first,
#                 'athlete_last_name': last,
#                 'team': result['team'],
#                 'meet_date': meet_date,
#                 'mark': result['mark'],
#                 'meet': meet,
#             }
#             mark_resp = requests.post(f"{SERVER_URL}/mark", json=mark_post_body)
#             mark_content = mark_resp.json()
#             if not mark_resp.ok and not mark_resp.status_code == 409:
#                 print(mark_content)
#                 x=1
#             if athlete_content.get('gender') is None:
#                 mark_params = {
#                     'athlete_uid': athlete_uid,
#                 }
#                 mark_filter_resp = requests.get(f"{SERVER_URL}/mark", params=mark_params)
#                 mark_filter_content = mark_filter_resp.json()

#                 athlete_content['gender'] = mark_filter_content['marks'][0]['gender']
#                 athlete_resp = requests.put(f"{SERVER_URL}/athlete", json=athlete_content)
#                 athlete_content = athlete_resp.json()
#             x=1
# x=1



