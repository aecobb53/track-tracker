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

x=1
