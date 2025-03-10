import os
import json
import requests
from datetime import datetime, timezone
from time import sleep


etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
BIG_ASS_JSON_PATH = os.path.join(etc_tmp, 'upload_file.json')
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


# resp = requests.get(f"{SERVER_URL}/result/")
# content= resp.json()
# x=1


runtime_start = datetime.now(timezone.utc)

with open(BIG_ASS_JSON_PATH, 'r') as jf:
    data = json.load(jf)

if os.path.exists(COMPLETED_STEPS):
    with open(COMPLETED_STEPS, 'r') as jf:
        progress_tracking = json.load(jf)
else:
    progress_tracking = {}


progress_count = sum([len(m) for y, m in data.items()])
progress_pointer = 0
x=1
for year, meets in data.items():
    if int(year) < 2025:
        continue
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
            for result in results:
                athlete = result.get('athlete')


                # Speeding up data uplaod
                if 'Fairview' not in athlete['team']:
                    continue




                result = result['result']

                event_query_params = {
                    'meet': result['meet'],
                    'event': result['event'],
                    'place': result['place'],
                    'team': result['team'],
                }
                existing_event_resp = requests.get(f"{SERVER_URL}/result/", params=event_query_params)
                existing_event_content = existing_event_resp.json()
                if existing_event_content.get('results') != []:
                    continue

                if athlete:
                    first = athlete['first_name']
                    last = athlete['last_name']
                    team = athlete['team']
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
                    elif athlete_resp.ok:
                        # Compare the athlete data
                        athlete_content = athlete_resp.json()
                        update = False
                        for key, value in athlete.items():
                            if athlete_content[key] != value:
                                # if key != 'graduation_year':
                                #     print('')
                                #     print('compared athletes but are different')
                                #     print(athlete_content)
                                #     print(athlete)
                                update = True
                                athlete_content[key] = value
                                x=1
                        if update:
                            x=1
                            athlete_resp = requests.put(f"{SERVER_URL}/athlete/", json=athlete_content)
                            if not athlete_resp.ok:
                                x=1
                                print(f"POST BODY: {athlete_content}")
                                raise ValueError('Failed to update athlete, investigate why')
                            x=1
                            athlete_content = athlete_resp.json()
                    else:
                        x=1
                    # athlete_content = athlete_resp.json()
                    if 'uid' not in athlete_content:
                        print(f"RESPONSE CODE: {athlete_resp.status_code}")
                        print(f"RESPONSE BODY: {athlete_content}")
                        raise ValueError('Athlete content does not have uid')
                    athlete_uid = athlete_content['uid']
                    result['athlete_uid'] = athlete_uid
                    result['athlete_first_name'] = first
                    result['athlete_last_name'] = last
                    x=1
                else:
                    # No athlete (Relay)
                    x=1
                result_resp = requests.post(f"{SERVER_URL}/result/", json=result)
                result_content = result_resp.json()
                if not result_resp.ok and result_resp.status_code != 409:
                    x=1
                x=1
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
