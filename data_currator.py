import os
import re
import json
import pyperclip


event_rename = {
    r'boys?': 'mens',
    r'girls?': 'womens',
    r'finals?': '',
    r'\da': '',
}


def rename_event(event):
    event = event.lower()
    for re_s, replace in event_rename.items():
        match = re.search(re_s, event)
        if match:
            event = re.sub(re_s, replace, event)
    event = event.strip().title()
    return event

with open('deleteme.json', 'r') as jf:
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

with open('deleteme2.json', 'w') as jf:
    jf.write(json.dumps(athletes, indent=4))
with open('deleteme3.json', 'w') as jf:
    jf.write(json.dumps(meets, indent=4))

# a = list(different_event_names)
# a.sort()
# for i in a:
#     print(i)

csv = ['Name,Event,Mark,Wind,Attempt,Year,Meet']
for athlete, events in athletes.items():
    
    if athlete == 'Relay':
        continue
    for event_name, results in events.items():
        for result in results:
            if result['mark'] is None:
                x=1
            data = [athlete]
            data.append(event_name)
            data.append(str(result['mark']))
            data.append(str(result['wind']))
            data.append(str(result['attempt']))
            data.append(str(result['calendar_year']))
            data.append(str(result['meet']))
            row_s = f','.join(data)
            row_s = row_s.replace('None', '-')
            csv.append(row_s)
pyperclip.copy('\n'.join(csv))

x=1
