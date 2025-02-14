import os
import re
import json


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

# for k, v in data.items():
#     if not v['raw']:
#         print(k)

athletes = {}
# different_event_names = set()
for meet, details in data.items():
    for event, results in details.items():
        if event == 'raw':
            continue
        for result in results:
            if 'Fairview High School' in result['team']:
                athlete = result.get('athlete', 'relay')
                event = rename_event(result['event'])
                result['meet'] = meet
                if athlete not in athletes:
                    athletes[athlete] = {}
                if result['event'] not in athletes[athlete]:
                    athletes[athlete][event] = []
                athletes[athlete][event].append(result)
                # different_event_names.add(event)
                
with open('deleteme2.json', 'w') as jf:
    jf.write(json.dumps(athletes, indent=4))

# a = list(different_event_names)
# a.sort()
# for i in a:
#     print(i)

x=1
