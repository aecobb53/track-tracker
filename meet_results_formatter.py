import os
import re
import json


def parse_data_row(data_row: list[str], event: str, header: list[str], calendar_year: int, meet_name: str):
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
            attempt = None
            year = None
            team = None
            mark = None
            wind_sign = None
            wind = None
            heat = None

            result_wind_re = re.search(r'[\s\t]+((\d+:)?\d+\.?\d*)[\s\t]+([-+])[\s\t]*(\d+.?\d*)[\s\t]+(\d+)', data_row[-1])
            result_no_wind_re = re.search(r'[\s\t]+((\d+:)?\d+?\.\d+)[\s\t]+(\d+)', data_row[-1])
            result_high_jump_re = re.search(r'[\s\t]+(\d+)-(\d+\.?\d*)[\s\t]+(\d+)', data_row[-1])
            result_long_jump_re = re.search(r'[\s\t]+(\d+)-(\d+\.?\d*)[\s\t]+([-+])(\d*\.?\d*)[\s\t]+(\d+)', data_row[-1])
            if result_wind_re:
                mark, _, wind_sign, wind, heat = result_wind_re.groups()
                team = data_row[-1][:result_wind_re.start(0)].strip()
            elif result_no_wind_re:
                mark, _, heat = result_no_wind_re.groups()
                team = data_row[-1][:result_no_wind_re.start(0)].strip()
            elif result_high_jump_re:
                attempt, mark, heat = result_high_jump_re.groups()
                team = data_row[-1][:result_high_jump_re.start(0)].strip()
            elif result_long_jump_re:
                attempt, mark, wind_sign, wind, heat = result_long_jump_re.groups()
                team = data_row[-1][:result_long_jump_re.start(0)].strip()
            else:
                x=1

            year_re = re.search(r'(\d+)', team)
            if year_re:
                year = int(year_re.groups()[0])
                team = team.replace(str(year), '').strip()

            if attempt:
                attempt = int(attempt)
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
                'attempt': attempt,
                'mark': mark,
                # 'wind_sign': wind_sign,
                'wind': wind,
                'heat': heat,
                'event': event
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

            if heat:
                heat = int(heat)
            data_obj = {
                'place': int(data_row[0]),
                'team': data_row[2],
                'mark': mark,
                'heat': heat,
                'event': event
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


def parse_meet_file(path: str):
    with open(path, 'r') as tf:
        data = [l[:-1] for l in tf.readlines()]
    meet_name = os.path.splitext(os.path.basename(path))[0]
    calendar_year = int(path[:4])

    event = None
    header = []
    meet_data = []
    data_row = []
    # for line in data:
    for index, line in enumerate(data):
        # if meet_name == 'Arcadia Invitational' and calendar_year == 2022 and index == 4510:
        #     x=1
        if 'All Results' in line or not line:
            continue
        newline_re = re.search(r'^\d+$', line.strip())
        if newline_re:
            row = parse_data_row(data_row=data_row, event=event, header=header, calendar_year=calendar_year, meet_name=meet_name)
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

            row = parse_data_row(data_row=data_row, event=event, header=header, calendar_year=calendar_year, meet_name=meet_name)
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
for item in os.listdir('.'):
    if item.endswith('_results'):
        meets_dirs.append(item)

meets_athlete_data = {}
for meets in meets_dirs:
    for meet in os.listdir(meets):
        results = parse_meet_file(path=os.path.join(meets, meet))
        meet_name = meet.replace('.txt','').strip()
        meets_athlete_data[meet_name] = results
with open('deleteme.json', 'w') as jf:
    jf.write(json.dumps(meets_athlete_data, indent=4))
x=1

"""
Its still transitioning poorly out of relay events. Maybe into them as well
"""
