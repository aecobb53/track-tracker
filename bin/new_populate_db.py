import os
import json
import requests
from datetime import datetime, timezone
from time import sleep
import re


etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
UPLOAD_DATA_PATH = os.path.join(etc_tmp, 'upload_file.json')
COMPLETED_STEPS = os.path.join(etc_tmp, 'workfile_deleteme_2025.json')
SERVER_URL = 'http://localhost:8205'
# SERVER_URL = 'https://fhs-track.nax.lol'
CURRENT_YEAR = 2025

YEAR_MAP = {
    9: 'Freshman',
    10: 'Sophomore',
    11: 'Junior',
    12: 'Senior',
}
sprint_tags = {
    r' 60 Meter': 'Sprint',
    r' 100 Meter': 'Sprint',
    r' 200 Meter': 'Sprint',
    r' 400 Meter': 'Sprint',
    r' 110 Meter': 'Sprint',
    r' 300 Meter': 'Sprint',
    r' 4x100 Meter': 'Sprint',
    r' 4x200 Meter': 'Sprint',
    r' 4x400 Meter': 'Sprint',
}
distance_tags = {
    r' 800 Meter': 'Distance',
    r' 1600 Meter': 'Distance',
    r' 3200 Meter': 'Distance',
    r' 4x800 Meter': 'Distance',
}
field_tags = {
    r' Jump': 'Field',
    r' Discus': 'Field',
    r' Shot Put': 'Field',
    r' Vault': 'Field',
}
relay_tags = {
    r' 4x100 Meter': 'Relay',
    r' 4x200 Meter': 'Relay',
    r' 4x400 Meter': 'Relay',
    r' 4x800 Meter': 'Relay',
}
tags_list = [
    sprint_tags,
    distance_tags,
    field_tags,
    relay_tags,
]

runtime_start = datetime.now(timezone.utc)

with open(UPLOAD_DATA_PATH, 'r') as jf:
    data = json.load(jf)

if os.path.exists(COMPLETED_STEPS):
    with open(COMPLETED_STEPS, 'r') as jf:
        progress_tracking = json.load(jf)
else:
    progress_tracking = {}
progress_tracking = {}


def upload_athlete(athlete, result):
    first = athlete['first_name']
    last = athlete['last_name']
    team = athlete['team']
    # Tags
    athlete_tags = []
    for tag_group in tags_list:
        for i, j in tag_group.items():
            if re.search(i, result['event']):
                athlete_tags.append(j)
                break
    athlete_tags = list(set(athlete.get('tags', []) + athlete_tags))
    athlete_tags.sort()
    athlete['tags'] = athlete_tags
    athlete_resp = requests.get(f"{SERVER_URL}/athlete/{first}/{last}/{team}/")
    if athlete_resp.status_code == 404:
        # Post new athlete
        athlete_resp = requests.post(f"{SERVER_URL}/athlete/", json=athlete)
        athlete_content = athlete_resp.json()
        if not athlete_resp.ok:
            search_params = {
                'first_name': first,
                'last_name': last,
                'team': team,
            }
            athlete_resp = requests.get(f"{SERVER_URL}/athlete/", params=search_params)
            athlete_content = athlete_resp.json()['athletes'][0]
        return athlete_content
    elif athlete_resp.ok:
        # Compare the athlete data
        athlete_content = athlete_resp.json()
        update = False
        for key, value in athlete.items():
            if athlete_content[key] != value:
                update = True
                if key == 'tags':
                    athlete_content[key] = athlete_content[key] + value
                else:
                    athlete_content[key] = value
        if update:
            # Need to update the record
            athlete_resp = requests.put(f"{SERVER_URL}/athlete/", json=athlete_content)
            if not athlete_resp.ok:
                print(f"POST BODY: {athlete_content}")
                raise ValueError('Failed to update athlete, investigate why')
            athlete_content = athlete_resp.json()
            return athlete_content
        else:
            return athlete_content
    else:
        x=1  # WHAT HAPPENED???
        raise ValueError('Failed to upload athlete, investigate why')
    return athlete_content



def upload_result(athlete_content, result):
    result['athlete_uid'] = athlete_content['uid']
    result['athlete_first_name'] = athlete_content['first_name']
    result['athlete_last_name'] = athlete_content['last_name']
    result_resp = requests.post(f"{SERVER_URL}/result/", json=result)
    result_content = result_resp.json()
    if not result_resp.ok and result_resp.status_code != 409:
        x=1
        raise ValueError('Failed to upload result, investigate why')
    return result_content

def upload_splits(relay_athletes):
    splits_content = []
    for item in relay_athletes:
        athlete = item['athlete']
        result = item['result']
        athlete_content = upload_athlete(athlete=athlete, result=result)
        result_content = upload_result(athlete_content=athlete_content, result=result)
        splits_content.append({
            'athlete_content': athlete_content,
            'result_content': result_content,
        })
    return splits_content


progress_count = sum([len(m) for y, m in data.items()])
progress_pointer = 0
x=1
for year, meets in data.items():
    if year not in progress_tracking:
        progress_tracking[year] = {}
    for meet_name, events in meets.items():
        if meet_name not in progress_tracking[year]:
            progress_tracking[year][meet_name] = {}
        if events is None:
            print(f"EVENTS ARE NONE THIS IS A PROBLEM BUT I NEED TO PUSH PAST")
            print(f"YEAR: {year}, MEET: {meet_name}")
            continue
        for event_name, results in events.items():
            if event_name not in progress_tracking[year][meet_name]:
                progress_tracking[year][meet_name][event_name] = False
            if progress_tracking[year][meet_name].get(event_name):
                continue
            x=1
            for result_item in results:
                athlete = result_item['athlete']
                result = result_item['result']
                relay_athletes = result_item.get('relay_athletes')




                # Speeding up data uplaod
                if 'Fairview' not in athlete['team']:
                    continue

                if 'Girls High Jump' in result['event']:
                    x=1


                event_query_params = {
                    'meet': result['meet'],
                    'event': result['event'],
                    'place': result['place'],
                    'team': result['team'],
                    'first_name': athlete['first_name'],
                    'last_name': athlete['last_name'],
                }
                existing_event_resp = requests.get(f"{SERVER_URL}/result/", params=event_query_params)
                existing_event_content = existing_event_resp.json()
                if existing_event_content.get('results') != []:
                    x=1
                    if relay_athletes:
                        splits_content = upload_splits(relay_athletes)
                    # Event already uploaded
                    continue

                athlete_content = upload_athlete(athlete=athlete, result=result)
                result_content = upload_result(athlete_content=athlete_content, result=result)
                x=1

                # # ADD RELAY ATHLETES STUFF HERE
                if relay_athletes:
                    splits_content = upload_splits(relay_athletes)
            progress_tracking[year][meet_name][event_name] = True
            with open(COMPLETED_STEPS, 'w') as jf:
                jf.write(json.dumps(progress_tracking, indent=4))
            sleep(1)
        x=1
        progress_pointer += 1
        percent_complete = int(progress_pointer / progress_count * 10000) / 100
        runtime_so_far = datetime.now(timezone.utc) - runtime_start
        print(f"Percent complete: {percent_complete}%, Time so far: {runtime_so_far}, Year: {year}, Meet: {meet_name}")
x=1

runtime_stop = datetime.now(timezone.utc)
print(f"RUNTIME: {runtime_start}, {runtime_stop}")
print(f"RUNTIME DIFF: {runtime_stop - runtime_start}")

x=1
