import requests
import json
import os
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

def make_call(url):
    resp = requests.get(url)
    content = resp.json()
    return resp, content

# resp, content = make_call(SERVER_URL)

pr_graph_resp, pr_graph_content = make_call(f'{SERVER_URL}/athlete/pr-graph')
x=1

meet_name_list = [
    'Coyote Invite',
    'BHS CHS FHS MHS',
    'Niwot',
    'BOCO Championships',
    'Centaurus Twilight',
    'Longmont Invitational',
    'League Championship',
    'St Vrain Last Chance',
    'Teddys Last Chance',
]
meet_name_dict = {m: {'Field': 0, 'Running': 0} for m in meet_name_list}


for athlete_graph in pr_graph_content['athletes_graph']:
    athlete = athlete_graph['athlete']
    results = athlete_graph['results']
    pr_data = athlete_graph['pr_data']
    for result in results:
        x=1
        if result['result_metadata'].get('PR'):
            field_strings = ['Jump', 'Shot', 'Vault', 'Discus']
            running_strings = ['Run', 'Dash', 'Hurdles']
            if any([i in result['event'] for i in field_strings]):
                thing = 'Field'
            elif any([i in result['event'] for i in running_strings]):
                thing = 'Running'
            elif 'Relay' in result['event']:
                continue
            else:
                print(f"IUSSUE WITH {result['event']}")
                
            meet_name_dict[result['meet']][thing] += 1
    x=1
x=1

for meet, deets in meet_name_dict.items():
    deets['total'] = sum(deets.values())

print(json.dumps(meet_name_dict, indent=4))
x=1


"""
Have to have
The total count of Field and Running PRs for each meet

Would like to have
Each Athletes PRs for each meet
"""

# athlete_resp, athlete_content = make_call(f'{SERVER_URL}/athlete')
# result_resp, result_content = make_call(f'{SERVER_URL}/result')

# data = {}
# for athlete in athlete_content['athletes']:
#     athlete['name'] = athlete['first_name'] + ' ' + athlete['last_name']
#     if athlete['uid'] not in data:
#         data[athlete['uid']] = {
#             'athlete': athlete,
#             'events': {},
#         }
#     for result in result_content['results']:
#         if result['athlete']['uid'] == athlete['uid']:
#             if result['event'] not in data[athlete['uid']]['events']:
#                 data[athlete['uid']]['events'][result['event']] = []
#             data[athlete['uid']]['events'][result['event']].append(result)
#             break
#     else:
#         x=1

# x=1

# # Order Athletes by name
# data = dict(sorted(data.items(), key=lambda item: item[1]['athlete']['last_name']))

# # Order Events by name
# for athlete in data:
#     data[athlete]['events'] = dict(sorted(data[athlete]['events'].items(), key=lambda item: item[0]))

# # Order Results by date
# for athlete in data:
#     for event in data[athlete]['events']:
#         data[athlete]['events'][event] = sorted(data[athlete]['events'][event], key=lambda x: x['meet_date'], reverse=True)

# x=1

# meet_name_list = [
#     'Coyote Invite',
#     'BHS CHS FHS MHS',
#     'Niwot',
#     'BOCO Championships',
#     'Centaurus Twilight',
#     'Longmont Invitational',
#     'League Championship',
#     'St Vrain Last Chance',
#     'Teddys Last Chance',
# ]

# # final_data = [[['First Name', 'Last Name', 'Gender'] + meet_name_list]]
# lines = []

# indent = '  '

# for athlete_uid, details in data.items():
#     athlete = details['athlete']
#     events = details['events']
#     events_dict = {}
#     lines.append(athlete['name'])
#     for event, results in events.items():
#         if event not in events_dict:
#             events_dict[event] = []
#         events_dict[event].extend(results)
#     # for event, results in events.items():
#     #     lines.append(f"{indent*1}{event}")
#     #     x=1
#     x=1









#     # final_data.append(lines)

# x=1
# for line in lines:
#     print(line)
# # for line in final_data:
# #     # print(line)
# #     for i in line:
# #         print(i)
# x=1
