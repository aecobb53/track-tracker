import os
import json
import requests
from datetime import datetime, timezone


etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
BIG_ASS_JSON_PATH = os.path.join(etc_tmp, 'BIG_ASS_JSON.json')
ATHLETE_JSON_PATH = os.path.join(etc_tmp, 'athlete.json')
SCHOOL_JSON_PATH = os.path.join(etc_tmp, 'school.json')
SERVER_URL = 'http://localhost:8205'
CURRENT_YEAR = 2025

YEAR_MAP = {
    9: 'Freshman',
    10: 'Sophomore',
    11: 'Junior',
    12: 'Senior',
}

def calculate_graduation_year(athlete_year: int, event_year: int):
    return event_year + 4 - athlete_year + 9

# DEBUG
resp = requests.get(f"{SERVER_URL}/athlete")
# resp = requests.get(f"{SERVER_URL}/athlete/Gordon/Nilsen/Fairview High School")
content = resp.json()
x=1
# DEBUG



testing = False
if testing:
    # Post Athlete
    with open(ATHLETE_JSON_PATH, 'r') as jf:
        data = json.load(jf)
    for name, events in data.items():
        first, last = name.split(' ')
        for event_name, results in events.items():
            for result in results:
                month, day = result['meet_metadata']['date'].split('/')
                meet_date = datetime(result['calendar_year'], int(month), int(day))
                meet_date = datetime.strftime(meet_date, '%Y-%m-%d')
                athlete_post_body = {
                    'first_name': first,
                    'last_name': last,
                    # 'year': YEAR_MAP[result['year']],
                    'team': result['team'],
                    'graduation_year': calculate_graduation_year(
                        athlete_year=result['year'],
                        event_year=result['calendar_year']),
                    'gender': 'FIX ME',
                }
                mark_post_body = {
                    'event': event_name,
                    'heat': result['heat'],
                    'place': result['place'],
                    'wind': result['wind'],
                    'attempt': result['attempt'],
                    # 'athlete': 'None',
                    'athlete_first_name': first,
                    'athlete_last_name': last,
                    'team': result['team'],
                    'meet_date': meet_date,
                    'mark': result['mark'],
                }
                break
        break

    resp = requests.get(f"{SERVER_URL}/athlete")
    content = resp.json()
    if len(content['athletes']) == 0:
        resp = requests.post(f"{SERVER_URL}/athlete", json=athlete_post_body)
        content = resp.json()
        print('POST')
        print(json.dumps(content, indent=4))
        x=1

    # get_params = {
    #     'first': athlete_post_body['first_name'],
    #     'last': athlete_post_body['last_name'],
    # }
    # resp = requests.post(f"{SERVER_URL}/athlete", json=athlete_post_body)
    # content = resp.json()
    # print('POST')
    # print(json.dumps(content, indent=4))

    # x=1

    # resp = requests.get(f"{SERVER_URL}/athlete")
    # content = resp.json()
    # print('GET')
    # print(json.dumps(content, indent=4))

    # x=1

    resp = requests.post(f"{SERVER_URL}/mark", json=mark_post_body)
    content = resp.json()
    print('POST')
    print(json.dumps(content, indent=4))

else:
    with open(ATHLETE_JSON_PATH, 'r') as jf:
        data = json.load(jf)
    for name, events in data.items():
        first_last = name.split(' ')
        first = first_last[0]
        last = ' '.join(first_last[1:])

        for event_name, results in events.items():
            for result in results:
                if not result['meet_metadata']:
                    continue
                month, day = result['meet_metadata']['date'].split('/')
                meet_date = datetime(result['calendar_year'], int(month), int(day))
                meet_date = datetime.strftime(meet_date, '%Y-%m-%d')

                athlete_resp = requests.get(f"{SERVER_URL}/athlete/{first}/{last}/{result['team']}")
                athlete_content = athlete_resp.json()
                if athlete_resp.status_code == 404:
                    # Need to add
                    athlete_post_body = {
                        'first_name': first,
                        'last_name': last,
                        'team': result['team'],
                        'graduation_year': calculate_graduation_year(
                            athlete_year=result['year'],
                            event_year=result['calendar_year']),
                        'gender': None,
                    }
                    athlete_resp = requests.post(f"{SERVER_URL}/athlete", json=athlete_post_body)
                    athlete_content = athlete_resp.json()
                athlete_uid = athlete_content['uid']
                mark_post_body = {
                    'event': event_name,
                    'heat': result['heat'],
                    'place': result['place'],
                    'wind': result['wind'],
                    'attempt': result['attempt'],
                    'athlete_uid': athlete_uid,
                    'athlete_first_name': first,
                    'athlete_last_name': last,
                    'team': result['team'],
                    'meet_date': meet_date,
                    'mark': result['mark'],
                    'meet': result['meet'],
                }
                mark_resp = requests.post(f"{SERVER_URL}/mark", json=mark_post_body)
                mark_content = mark_resp.json()
                if not mark_resp.ok:
                    x=1
                if athlete_content['gender'] is None:
                    mark_params = {
                        'athlete_uid': athlete_uid,
                    }
                    mark_filter_resp = requests.get(f"{SERVER_URL}/mark", params=mark_params)
                    mark_filter_content = mark_filter_resp.json()

                    athlete_content['gender'] = mark_filter_content['marks'][0]['gender']
                    athlete_resp = requests.put(f"{SERVER_URL}/athlete", json=athlete_content)
                    athlete_content = athlete_resp.json()
                x=1

x=1
