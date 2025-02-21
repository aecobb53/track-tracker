import os
import re
import json


etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
MEET_DATES_PATH = os.path.join(etc_tmp, 'meet_dates.json')
OUTPUT_PATH = os.path.join(etc_tmp, 'upload_file.json')


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
            student_year = None
            year = None
            team = None
            mark = None
            wind_sign = None
            wind = None
            heat = None
            gender = None
            graduation_year = None
            result_run_re = re.search(r'[\s\t]+(\d*:?\d+\.?\d*)[\s\t]+([-+])?(\d*\.?\d*)?[\s\t]*(\d+)', data_row[-1])
            result_jump_re = re.search(r'[\s\t]+(\d+-\d+\.?\d*)[\s\t]+([-+])?(\d*\.?\d*)?[\s\t]*(\d+)', data_row[-1])

            place = int(data_row[0])
            first_last = data_row[1].split(' ')
            first = first_last[0]
            last = ' '.join(first_last[1:])

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
            place = int(place)
            meet_date = f"{calendar_year}-{meet_metadata['date'].replace('/', '-')}"

            # Gender
            re_strings = {
                r'(Boys?|Mens?)': 'Mens',
                r'(Girls?|Womens?)': 'Womens',
            }
            for re_string, gender_string in re_strings.items():
                if re.search(re_string, event):
                    gender = gender_string
                    break

            # Graduation Year
            if year:
                graduation_year = calendar_year + (12 - year)
                if year == 12:
                    assert graduation_year == calendar_year
                elif year == 11:
                    assert graduation_year == calendar_year + 1
                elif year == 10:
                    assert graduation_year == calendar_year + 2
                elif year == 9:
                    assert graduation_year == calendar_year + 3
            else:
                graduation_year = None

            athlete_data = {
                'first_name': first,
                'last_name': last,
                'team': team,
                'gender': gender,
                'graduation_year': graduation_year,
            }

            interigate_data = {k: v for k, v in athlete_data.items() if k not in ['graduation_year']}
            if any([True for v in interigate_data.values() if v is None]):
                x=1

            mark_data = {
                'event': event,
                'heat': heat,
                'place': place,
                'wind': wind,
                'team': team,
                'meet_date': meet_date,
                'mark': mark,
                'meet': meet_name,
                'gender': gender,
            }

            interigate_data = {k: v for k, v in mark_data.items() if k not in ['year']}
            if any([True for v in interigate_data.values() if v is None]):
                x=1

            data_obj = {
                'athlete': athlete_data,
                'mark': mark_data,
            }
            return data_obj
        else:
            x=1
    elif len(header) == 5 and len(data_row) == 3:
        if header == ['PLACE', 'VIDEO', 'TEAM', 'MARK', 'HEAT']:
            heat = None
            place = None
            wind = None
            team = None
            meet_date = None
            mark = None
            gender = None

            result_relay_re = re.search(r'((\d+:)?\d+\.?\d*)[\s\t]+(\d+)', data_row[-1])
            if result_relay_re:
                mark, _, heat = result_relay_re.groups()
            else:
                x=1
            team = data_row[-2]

            if heat:
                heat = int(heat)
            place = int(data_row[0])
            meet_date = f"{calendar_year}-{meet_metadata['date'].replace('/', '-')}"

            # Gender
            re_strings = {
                r'(Boys?|Mens?)': 'Mens',
                r'(Girls?|Womens?)': 'Womens',
            }
            for re_string, gender_string in re_strings.items():
                if re.search(re_string, event):
                    gender = gender_string
                    break

            # data_obj = {
            #     'place': data_row[0],
            #     'calendar_year': calendar_year,
            #     'team': team,
            #     'mark': mark,
            #     'heat': heat,
            #     'event': event,
            #     'meet_metadata': meet_metadata,
            #     'wind': 0.0,
            # }

            # interigate_data = {k: v for k, v in data_obj.items() if k not in ['year']}
            # if any([True for v in interigate_data.values() if v is None]):
            #     x=1

            athlete_data = {
                'first_name': team,
                'last_name': f"{gender} Relay",
                'team': team,
                'gender': gender,
                'graduation_year': calendar_year,
            }

            mark_data = {
                'event': event,
                'heat': heat,
                'place': place,
                'wind': wind,
                'team': team,
                'meet_date': meet_date,
                'mark': mark,
                'meet': meet_name,
                'gender': gender,
            }

            interigate_data = {k: v for k, v in mark_data.items() if k not in ['wind']}
            if any([True for v in interigate_data.values() if v is None]):
                x=1

            data_obj = {
                'athlete': athlete_data,
                'mark': mark_data,
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


def parse_meet_file(path: str, meet_name: str, meet_dates: dict):
    with open(path, 'r') as tf:
        data = [l[:-1] for l in tf.readlines()]
    # meet_name = os.path.splitext(os.path.basename(path))[0]
    calendar_year = int(path.split('/')[-2][5:9])

    event = None
    header = []
    meet_data = []
    data_row = []
    for _, deets in meet_dates.get(str(calendar_year), {}).items():
        if os.path.basename(path) == deets['filename']:
            meet_metadata = {
                'date': deets['date'],
                'meet_name': deets['meet'],
                'location': deets['location']
            }
            break
    else:
        print(f"FAILED TO FIND MEET DATA FOR {path}")
        meet_metadata = None
        return None

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

    output_data = {}
    for record in meet_data:
        if record['mark']['event'] not in output_data:
            output_data[record['mark']['event']] = []
        output_data[record['mark']['event']].append(record)
    return output_data

meets_dirs = []
for item in os.listdir(etc_dir):
    if item.endswith('_results'):
        meets_dirs.append(os.path.join(etc_dir, item))

with open(MEET_DATES_PATH, 'r') as jf:
    meet_dates = json.loads(jf.read())

meets_results = {}
for meets in meets_dirs:
    for meet in os.listdir(meets):
        meet_filepath = os.path.join(meets, meet)
        meet_name = meet.replace('.txt','').strip()
        meet_year = int(meet_filepath.split('/')[-2][:4])
        results = parse_meet_file(path=meet_filepath, meet_name=meet_name, meet_dates=meet_dates)
        if meet_year not in meets_results:
            meets_results[meet_year] = {}
        meets_results[meet_year][meet_name] = results

# Ordering
years = list(meets_results.keys())
years.sort()
data_to_dump = {year: meets_results[year] for year in years}

with open(OUTPUT_PATH, 'w') as jf:
    jf.write(json.dumps(data_to_dump, indent=4))
x=1
