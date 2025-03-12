import os
import json
import requests
from datetime import datetime, timezone
from time import sleep

etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
etc_workouts = os.path.join(etc_dir, 'workouts')
BIG_ASS_JSON_PATH = os.path.join(etc_tmp, 'upload_file.json')
COMPLETED_STEPS = os.path.join(etc_tmp, 'workfile_deleteme3.json')
SERVER_URL = 'http://localhost:8205'
SERVER_URL = 'https://fhs-track.nax.lol'
TEAM = 'Fairview High School'


def format_upload_from_csv(workout_date, workout_file, workout_name, workout_description):
    with open(workout_file, 'r') as wf:
        csv = [l[:-1].split(',') for l in wf.readlines()]
    keys = csv.pop(0)
    if ('First Name' not in keys and 'Last Name' not in keys) and ('First' not in keys and 'Last' not in keys):
        x=1
        if keys[0] != 'Athlete':
            'There just needs to be an Athlete field to know who to tie it to'
            raise ValueError('Im not sure how to interpret this header appropriately: {keys}')
    workout_results = []
    for row in csv:
        workout_row = {k: v for k, v in zip(keys, row)}
        first_name = workout_row.get('First Name', None)
        last_name = workout_row.get('Last Name', None)

        if not first_name:
            first_name = workout_row.get('First', None)
        if not last_name:
            last_name = workout_row.get('Last', None)


        if not first_name and not last_name:
            first_last = workout_row.pop('Athlete')
            first_name = first_last.split()[0]
            last_name = ' '.join(first_last.split()[1:])

        if not last_name:
            last_name = 'Doe'

        workout_row['first_name'] = first_name.strip()
        workout_row['last_name'] = last_name.strip()
        workout_results.append(workout_row)
    return workout_results

# def display_workout(workout_results):
#     pass

def upload_data(workout_results, workout_date, workout_name, workout_description, tags):
    for row in workout_results:
        first = row['first_name']
        last = row['last_name']
        if not last:
            last = 'Doe'
        athlete_resp = requests.get(f"{SERVER_URL}/athlete/{first}/{last}/{TEAM}")
        # print(athlete_resp.content)
        # athlete_content = athlete_resp.json()
        if athlete_resp.status_code == 400:
            resp = requests.get(f"{SERVER_URL}/athlete/", params={
                'first_name': first,
                'last_name': last,
                'team': TEAM,
            })
            content = resp.json()
            athlete_content = content['athletes'][0]
            X=1
        elif not athlete_resp.ok:
            # Need to create a new athlete
            athlete_payload = {
                'first_name': first,
                'last_name': last,
                'team': TEAM,
            }
            athlete_resp = requests.post(f"{SERVER_URL}/athlete/", json=athlete_payload)
            athlete_content = athlete_resp.json()
        elif athlete_resp.ok:
            athlete_content = athlete_resp.json()
            for tag in tags:
                if tag not in athlete_content['tags']:
                    x=1
                    athlete_content['tags'] = athlete_content['tags'] + tags
                    athlete_resp = requests.put(f"{SERVER_URL}/athlete/", json=athlete_content)
                    athlete_content = athlete_resp.json()
                    break
            x=1
        else:
            athlete_content = athlete_resp.json()

        skip_keys = ['first_name', 'last_name', 'First', 'Last', 'First Name', 'Last Name']
        results = {}
        results = {k: v for k, v in row.items() if k not in skip_keys}
        print(f"KEYS: {results.keys()}")

        workout_payload = {
            'results': results,
            'workout': workout_name,
            'workout_description': workout_description,
            'workout_date': workout_date,
            'athlete_uid': athlete_content['uid'],
            'athlete_first_name': athlete_content['first_name'],
            'athlete_last_name': athlete_content['last_name'],
        }
        workout_resp = requests.post(f"{SERVER_URL}/workout/", json=workout_payload)
        if workout_resp.status_code == 409:
            params = {
                'workout': workout_name,
                'workout_date': [
                    f"After{workout_date}",
                    f"Before{workout_date}",
                ],
                'athlete_uid': [athlete_content['uid']],
            }
            workout_resp = requests.get(f"{SERVER_URL}/workout/", params=params)
            if workout_resp.json().get('workouts'):
                workout_content = workout_resp.json()['workouts'][0]
        elif not workout_resp.ok:
            workout_content = workout_resp.json()
            x=1
            raise ValueError(f"Could not upload workout {workout_payload}")
        else:
            workout_content = workout_resp.json()
    x=1

workout_resp = requests.get(f"{SERVER_URL}/workout/")
workout_content = workout_resp.json()
# with open('deleteme.json', 'w') as f:
#     f.write(json.dumps(workout_content, indent=4))
x=1

tags = ['Sprint']

# Workout 1
workout_date = datetime.strftime(datetime(2025,2,24), "%Y-%m-%d")
workout_file = os.path.join(etc_workouts, 'w1_10x200.csv')
workout_name = '10x200 Meter Repeats'
workout_description = '10 by 200m repeats'

workout_results = format_upload_from_csv(workout_date, workout_file, workout_name, workout_description)
# display_workout(workout_results)
upload_data(workout_results, workout_date, workout_name, workout_description, tags)


# Time Trial 1
workout_date = datetime.strftime(datetime(2025,2,28), "%Y-%m-%d")
workout_file = os.path.join(etc_workouts, 'w2_300.csv')
workout_name = '300 Meter Time Trial'
workout_description = '300 Meter Pres Season Time Trial'

workout_results = format_upload_from_csv(workout_date, workout_file, workout_name, workout_description)
# display_workout(workout_results)
upload_data(workout_results, workout_date, workout_name, workout_description, tags)

# Workout 2
workout_date = datetime.strftime(datetime(2025,3,3), "%Y-%m-%d")
workout_file = os.path.join(etc_workouts, 'w3_10x200.csv')
workout_name = '10x200 Meter Repeats'
workout_description = '10 by 200m repeats'

workout_results = format_upload_from_csv(workout_date, workout_file, workout_name, workout_description)
# display_workout(workout_results)
upload_data(workout_results, workout_date, workout_name, workout_description, tags)

# Workout 3
workout_date = datetime.strftime(datetime(2025,3,5), "%Y-%m-%d")
workout_file = os.path.join(etc_workouts, 'w4_4x400.csv')
workout_name = '4x400 Meter Repeats'
workout_description = '4 by 400m repeats'

workout_results = format_upload_from_csv(workout_date, workout_file, workout_name, workout_description)
# display_workout(workout_results)
upload_data(workout_results, workout_date, workout_name, workout_description, tags)
x=1



"""
Aliases
Dash - Dashiel
"""


