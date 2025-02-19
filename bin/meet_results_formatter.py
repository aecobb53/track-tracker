import os
import re
import json


etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
MEET_DATES_PATH = os.path.join(etc_tmp, 'meet_dates.json')
BIG_ASS_JSON_PATH = os.path.join(etc_tmp, 'BIG_ASS_JSON.json')



with open(BIG_ASS_JSON_PATH, 'r') as jf:
    fuck = json.load(jf)

# for meet, events in fuck.items():
#     x=1
#     for event_name, places in events.items():
#         x=1
#         for shit in places:
#             if re.search(r'\d', shit['team']):
#                 team = shit['team']
#                 event = shit['event']
#                 meet = shit['meet_metadata']['meet_name']
#                 if team == '127 Project':
#                     pass
#                 elif team == 'Columbia (Sec 2)':
#                     pass
#                 else:
#                     x=1
#     # for event in meets_athlete_data[meet]:
#     #     for record in meets_athlete_data[meet][event]:
#     #         if record['mark']:
#     #             if ':' in record['mark']:
#     #                 x=1
#     #             else:
#     #                 x=1
#     #         else:
#     #             x=1

# x=1




def parse_data_row(data_row: list[str], event: str, header: list[str], calendar_year: int, meet_name: str, meet_metadata: dict):
    # New result indicator
    if len(data_row) == 5 and data_row[-1] == '':
        data_row.pop(-1)
    # if len(data_row) == 3:
    #     # Missing video column
    #     if data_row[1] != '':
    #         data_row.insert(1, '')

    if not event:
        return None
    if 'decathlon' in event.lower():
        # PARSE AT SOME POINT
        return None
    if 'heptathlon' in event.lower():
        # PARSE AT SOME POINT
        return None

    A_header_len = len(header)
    A_row_len = len(data_row)
    if len(header) == 7 and len(data_row) == 3:
        if header == ['PLACE', 'VIDEO', 'ATHLETE', 'TEAM', 'MARK', 'WIND', 'HEAT']:
            year = None
            team = None
            mark = None
            wind_sign = None
            wind = None
            heat = None
            result_run_re = re.search(r'[\s\t]+(\d*:?\d+\.?\d*)[\s\t]+([-+])?(\d*\.?\d*)?[\s\t]*(\d+)', data_row[-1])
            result_jump_re = re.search(r'[\s\t]+(\d+-\d+\.?\d*)[\s\t]+([-+])?(\d*\.?\d*)?[\s\t]*(\d+)', data_row[-1])
            # result_jump_re = re.search(r'[\s\t]+(\d+-?\d+\.?\d*)[\s\t]+([-+])?(\d*\.?\d*)?[\s\t]*(\d+)', data_row[-1])


            # if 'Kaleb Kimaita' in data_row[1] and 'Erie' in meet_metadata['meet_name']:
            #     x=1


            if result_jump_re:
                mark, wind_sign, wind, heat = result_jump_re.groups()
                team = data_row[-1][:result_jump_re.start(0)].strip()
            elif result_run_re:
                mark, wind_sign, wind, heat = result_run_re.groups()
                team = data_row[-1][:result_run_re.start(0)].strip()
            else:
                x=1

            year_re = re.search(r'(\d+)', team)
            if year_re:
                year = int(year_re.groups()[0])
                team = team.replace(str(year), '').strip()

            if wind:
                wind = float(wind)
            if wind_sign:
                if wind_sign == '-':
                    wind = -wind
            if heat:
                heat = int(heat)

            data_obj = {
                'place': int(data_row[0]),
                'athlete': data_row[1],
                'year': year,
                'calendar_year': calendar_year,
                'team': team,
                'mark': mark,
                'wind': wind,
                'heat': heat,
                'event': event,
                'meet_metadata': meet_metadata,
            }
            return data_obj
    elif len(header) == 5 and len(data_row) == 3:
        if header == ['PLACE', 'VIDEO', 'TEAM', 'MARK', 'HEAT']:
            mark = None
            heat = None

            result_relay_re = re.search(r'((\d+:)?\d+\.?\d*)[\s\t]+(\d+)', data_row[-1])
            if result_relay_re:
                mark, _, heat = result_relay_re.groups()
            else:
                x=1
            team = data_row[-2]

            if heat:
                heat = int(heat)
            data_obj = {
                'place': int(data_row[0]),
                'calendar_year': calendar_year,
                'team': team,
                'mark': mark,
                'heat': heat,
                'event': event,
                'meet_metadata': meet_metadata,
                'wind': 0.0,
            }
            return data_obj
        else:
            xc=1
    else:
        if data_row:
            if 'PLACE' not in data_row[-1]:
                x=1
            x=1
        return None


def parse_meet_file(path: str, meet_dates: dict):
    with open(path, 'r') as tf:
        data = [l[:-1] for l in tf.readlines()]
    meet_name = os.path.splitext(os.path.basename(path))[0]
    calendar_year = int(path.split('/')[-2][:4])

    event = None
    header = []
    meet_data = []
    data_row = []
    for date, deets in meet_dates.get(str(calendar_year), {}).items():
        if  os.path.basename(path) == deets['filename']:
            meet_metadata = {
                'date': deets['date'],
                'meet_name': deets['meet'],
                'location': deets['location']
            }
            break
    else:
        meet_metadata = None

    for index, line in enumerate(data):
        if 'All Results' in line or not line:
            continue
        newline_re = re.search(r'^\d+$', line.strip())
        if newline_re:
            row = parse_data_row(data_row=data_row, event=event, header=header, calendar_year=calendar_year, meet_name=meet_name, meet_metadata=meet_metadata)
            if row:
                meet_data.append(row)
            data_row = []

        if event and header:
            data_row.append(line)

        re_strings = (
            '^boys? ',
            '^girls? ',
            '^mens? ',
            '^womens? ',
            ' boys? ',
            ' girls? ',
            ' mens? ',
            ' womens? ',
            )
        re_skip_strings = (
            'girls? academic',
        )
        if any([re.search(i, line.replace("'", '').strip().lower()) for i in re_strings]) and not any([re.search(i, line.replace("'", '').strip().lower()) for i in re_skip_strings]):
            if data_row:
                data_row.pop(-1)

            row = parse_data_row(data_row=data_row, event=event, header=header, calendar_year=calendar_year, meet_name=meet_name, meet_metadata=meet_metadata)
            if row:
                meet_data.append(row)
            data_row = []
            event = line
        if line.strip().lower().startswith(('place')):
            header = [l.strip() for l in line.split(' ')]

    return_object = {}
    for record in meet_data:
        if record['event'] not in return_object:
            return_object[record['event']] = []
        return_object[record['event']].append(record)
    return_object['raw'] = meet_data
    return return_object

meets_dirs = []
for item in os.listdir(etc_dir):
    if item.endswith('_results'):
        meets_dirs.append(os.path.join(etc_dir, item))

with open(MEET_DATES_PATH, 'r') as jf:
    meet_dates = json.loads(jf.read())

meets_athlete_data = {}
for meets in meets_dirs:
    for meet in os.listdir(meets):
        results = parse_meet_file(path=os.path.join(meets, meet), meet_dates=meet_dates)
        meet_name = meet.replace('.txt','').strip()
        meets_athlete_data[meet_name] = results
with open(BIG_ASS_JSON_PATH, 'w') as jf:
    jf.write(json.dumps(meets_athlete_data, indent=4))
x=1
