from calendar import calendar
import os
import re
import json
import pyperclip
from datetime import datetime


event_rename = {
    r'boys?': 'mens',
    r'girls?': 'womens',
    r'finals?': '',
    r'varsity': '',
    r'emerging elite': '',
    r'championship': '',
    r'\da': '',
}
etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
BIG_ASS_JSON_PATH = os.path.join(etc_tmp, 'BIG_ASS_JSON.json')
ATHLETE_JSON_PATH = os.path.join(etc_tmp, 'athlete.json')
SCHOOL_JSON_PATH = os.path.join(etc_tmp, 'school.json')


def rename_event(event):
    event = event.lower()
    for re_s, replace in event_rename.items():
        match = re.search(re_s, event)
        if match:
            event = re.sub(re_s, replace, event)
    event = event.strip().title()
    return event

with open(BIG_ASS_JSON_PATH, 'r') as jf:
    data = json.load(jf)

athletes = {}
different_event_names = set()
for meet, details in data.items():
    for event, results in details.items():
        if event == 'raw':
            continue
        for result in results:
            if 'Fairview High School' in result['team']:
                athlete = result.get('athlete', 'Relay')
                event = rename_event(result['event'])
                result['meet'] = meet
                if athlete not in athletes:
                    athletes[athlete] = {}
                if event not in athletes[athlete]:
                    athletes[athlete][event] = []
                athletes[athlete][event].append(result)
                different_event_names.add(event)

meets = {}
for meet, details in data.items():
    for event, results in details.items():
        if event == 'raw':
            continue
        for result in results:
            if 'Fairview High School' in result['team']:
                athlete = result.get('athlete', 'Relay')
                event = rename_event(result['event'])
                result['meet'] = meet
                if meet not in meets:
                    meets[meet] = {}
                if event not in meets[meet]:
                    meets[meet][event] = []
                meets[meet][event].append(result)
                # different_event_names.add(event)

with open(ATHLETE_JSON_PATH, 'w') as jf:
    jf.write(json.dumps(athletes, indent=4))
with open(SCHOOL_JSON_PATH, 'w') as jf:
    jf.write(json.dumps(meets, indent=4))


a = list(different_event_names)
a.sort()
for i in a:
    print(i)

csv = ['Name,Event,Mark,Wind,Attempt,Year,Date,Meet']
for athlete, events in athletes.items():
    if athlete == 'Relay':
        continue
    for event_name, results in events.items():
        for result in results:
            if result.get('meet_metadata'):
                month, day = result['meet_metadata']['date'].split('/')
                date = datetime(int(result['calendar_year']), int(month), int(day))
                date = date.strftime('%m/%d/%Y')
            else:
                date = None
            data = [athlete]
            data.append(event_name)
            data.append(str(result['mark']))
            data.append(str(result['wind']))
            # data.append(str(result['attempt']))
            data.append(str(result['calendar_year']))
            data.append(str(date))
            data.append(str(result['meet']))
            row_s = f','.join(data)
            row_s = row_s.replace('None', '-')
            csv.append(row_s)
pyperclip.copy('\n'.join(csv))

x=1
