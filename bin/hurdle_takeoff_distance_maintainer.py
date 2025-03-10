import requests
import re
import json


TEAM = 'Fairview High School'
URL = 'http://localhost:8205'
# URL = 'https://fhs-track.nax.lol'

data = [
    {
        'first_name': 'Elise',
        'last_name': 'Roehrich',
        'graduation_year': 2027,
        'team': TEAM,
        'gender': 'Girls',
        'tags': ['Sprint'],
        'athlete_metadata': {
            'Takeoff': '2\' 3"'
        },
    },
    {
        'first_name': 'Domenica',
        'last_name': 'Plaza Homiston',
        'graduation_year': 2027,
        'team': TEAM,
        'gender': 'Girls',
        'tags': ['Sprint'],
        'athlete_metadata': {
            'Takeoff': '1\' 6"'
        },
    },
    {
        'first_name': 'Hilary',
        'last_name': 'Bojar',
        'athlete_metadata': {
            'Takeoff': '2\' 9"'
        },
    },
    {
        'first_name': 'Isabela',
        'last_name': '',
        'athlete_metadata': {
            'Takeoff': '1\' 6"'
        },
    },
    {
        'first_name': 'James',
        'last_name': '', #'Lawson',
        'athlete_metadata': {
            'Takeoff': '4\' 1"'
        },
    },
    {
        'first_name': 'Christopher',
        'last_name': 'McCutcheon',
        'graduation_year': 2027,
        'team': TEAM,
        'gender': 'Boys',
        'tags': ['Sprint'],
        'athlete_metadata': {
            'Takeoff': '3\' 5"'
        },
    },
    {
        'first_name': 'Caden',
        'last_name': 'Rozic',
        'graduation_year': 2027,
        'team': TEAM,
        'gender': 'Boys',
        'tags': ['Sprint'],
        'athlete_metadata': {
            'Takeoff': '3\' 2"'
        },
    },
]

for athlete in data:
    first = athlete['first_name']
    last = athlete['last_name']
    athlete_metadata = athlete['athlete_metadata']
    if not last:
        continue

    athlete_resp = requests.get(f"{URL}/athlete/{first}/{last}/{TEAM}/")
    if athlete_resp.ok:
        athlete_content = athlete_resp.json()
        athlete_content['athlete_metadata'].update(athlete_metadata)
        athlete_resp = requests.put(f"{URL}/athlete/", json=athlete_content)
    elif athlete_resp.status_code == 404:
        athlete_resp = requests.post(f"{URL}/athlete/", json=athlete)
        x=1
    else:
        x=1
    # athlete_content['takeoff_distance'] = takeoff
    # athlete_resp = requests.put(f"{URL}/athlete/{first}/{last}/", json=athlete_content)
    # print(json.dumps(athlete_resp.json(), indent=4))
x=1
