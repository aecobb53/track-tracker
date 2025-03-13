from calendar import calendar
import os
import re
import json
import yaml
from datetime import datetime, timedelta

etc_dir = 'etc'
etc_tmp = os.path.join(etc_dir, 'tmp')
MEET_DATES_PATH = os.path.join(etc_tmp, 'meet_dates.json')
OUTPUT_PATH = os.path.join(etc_tmp, 'upload_file.json')
DATE_RANGE_START = datetime(2025,1,1,)  # Or None
TEAM = 'Fairview High School'
points = [  # For meets with three or less teams
    5,
    3,
    1
]
NORMAL_POINTS = [
    10,
    8,
    6,
    5,
    4,
    3,
    2,
    1,
]
SMALL_POINTS = [
    5,
    3,
    1,
]

def assess_points(event: str, place: int, tri_meet: bool = False):
    if tri_meet:
        if place < len(SMALL_POINTS) + 1:
            return SMALL_POINTS[place - 1]
    else:
        if place < len(NORMAL_POINTS) + 1:
            return NORMAL_POINTS[place - 1]
    return 0

def parse_event_time(time):
    a = time.split(':')
    if len(a) == 2:
        minutes = int(a.pop(0))
    else:
        minutes = 0
    seconds = float(a[0]) + ( 60 * minutes )
    return seconds

def parse_data_row(
    data_row: list[str],
    event: str,
    header: list[str],
    calendar_year: int,
    meet_name: str,
    meet_metadata: dict,
    relay_data: dict,
    tri_meet):
    # New result indicator
    if len(data_row) == 5 and data_row[-1] == '':
        data_row.pop(-1)
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
            result = None
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
                result, wind_sign, wind, heat = result_jump_re.groups()
                team = data_row[-1][:result_jump_re.start(0)].strip()
            elif result_run_re:
                result, wind_sign, wind, heat = result_run_re.groups()
                team = data_row[-1][:result_run_re.start(0)].strip()
            else:
                if '9:54:' in data_row[-1]:
                    return  # There were some VERY bad results in one meet
                x=1
                return

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
            re_gender_strings = {
                r'(Boys?|Mens?)': 'Boys',
                r'(Girls?|Womens?)': 'Girls',
            }
            for re_string, gender_string in re_gender_strings.items():
                if re.search(re_string, event):
                    gender = gender_string
                    break

            # Event Rename
            re_event_strings = {
                r'100 Meter Dash': '100 Meter Dash',
                r'120 Meter Dash': '120 Meter Dash',
                r'200 Meter Dash': '200 Meter Dash',
                r'400 Meter Dash': '400 Meter Dash',
                r'800 Meter Run': '800 Meter Run',
                r'1500 Meter Run': '1500 Meter Run',
                r'1600 Meter Run': '1600 Meter Run',
                r'3000 Meter Run': '3000 Meter Run',
                r'3200 Meter Run': '3200 Meter Run',
                r'5000 Meter Run': '5000 Meter Run',
                r'One Mile Run': 'One Mile Run',
                r'2 Mile Run': '2 Mile Run',
                r'100 Meter Hurdles': '100 Meter Hurdles',
                r'110 Meter Hurdles': '110 Meter Hurdles',
                r'300 Meter Hurdles': '300 Meter Hurdles',
                r'400 Meter Hurdles': '400 Meter Hurdles',
                r'High Jump': 'High Jump',
                r'Long Jump': 'Long Jump',
                r'Triple Jump': 'Triple Jump',
                r'Pole Vault': 'Pole Vault',
                r'Discus': 'Discus',
                r'Shot Put': 'Shot Put',
                r'Javelin': 'Javelin',
                r'Hammer Throw': 'Hammer Throw',
                r'100 Meter Wheelchair Race': '100 Meter Wheelchair Race',
                r'200 Meter Wheelchair Race': '200 Meter Wheelchair Race',
                r'2000 Meter Steeplechase': '2000 Meter Steeplechase',
                r'3000 Meter Racewalk': '3000 Meter Racewalk',
            }
            for re_event, replace in re_event_strings.items():
                if re.search(re_event, event):
                    event = f"{gender} {replace}"
                    break
            else:
                raise ValueError(f"EVENT UNKNOWN: {event}")

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

            points = assess_points(event=event, place=place, tri_meet=tri_meet)

            result_data = {
                'event': event,
                'heat': heat,
                'place': place,
                'wind': wind,
                'team': team,
                'points': points,
                'meet_date': meet_date,
                'result': result,
                'meet': meet_name,
                'gender': gender,
            }

            data_obj = {
                'athlete': athlete_data,
                'result': result_data,
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
            result = None
            gender = None

            result_relay_re = re.search(r'((\d+:)?\d+\.?\d*)[\s\t]+(\d+)', data_row[-1])
            if result_relay_re:
                result, _, heat = result_relay_re.groups()
            else:
                x=1
            team = data_row[-2]

            if heat:
                heat = int(heat)
            place = int(data_row[0])
            meet_date = f"{calendar_year}-{meet_metadata['date'].replace('/', '-')}"

            # Gender
            re_strings = {
                r'(Boys?|Mens?)': 'Boys',
                r'(Girls?|Womens?)': 'Girls',
            }
            for re_string, gender_string in re_strings.items():
                if re.search(re_string, event):
                    gender = gender_string
                    break

            # Event Rename
            re_event_strings = {
                r'4x100 Meter Relay': '4x100 Meter Relay',
                r'4x200 Meter Relay': '4x200 Meter Relay',
                r'4x400 Meter Relay': '4x400 Meter Relay',
                r'4x800 Meter Relay': '4x800 Meter Relay',
                r'Sprint Medley Relay': 'Sprint Medley Relay',
                r'4xMile Relay': '4xMile Relay',
                r'4x100 Meter Throwers Relay': '4x100 Meter Throwers Relay',
                r'4x110 Shuttle Hurdle Relay': '4x110 Shuttle Hurdle Relay',
                r'4x100 Shuttle Hurdle Relay': '4x100 Shuttle Hurdle Relay',
                r'4x1600 Meter Relay': '4x1600 Meter Relay',
                r'Distance Medley Relay': 'Distance Medley Relay',
            }
            for re_event, replace in re_event_strings.items():
                if re.search(re_event, event):
                    event = f"{gender} {replace}"
                    break
            else:
                raise ValueError(f"EVENT UNKNOWN: {event}")

            athlete_data = {
                'first_name': team,
                'last_name': f"{gender} Relay",
                'team': team,
                'gender': gender,
                'graduation_year': calendar_year,
            }

            points = assess_points(event=event, place=place, tri_meet=tri_meet)
            # Add data for relay legs
            relay_athletes_dict = []
            if team == TEAM and relay_data:
                for relay_i in range(len(relay_data[gender])):
                    relay = relay_data[gender][relay_i]
                    if relay['relay'] in event:
                        relay = relay_data[gender].pop(relay_i)
                        if any([True for athlete in [relay[i] for i in [1, 2, 3, 4]] if athlete['split'] is None]):
                            # There are some None splits
                            remaining_time = str(relay['time'])
                            seconds = parse_event_time(remaining_time)
                            for timed_athlete in [
                                athlete for athlete in [relay[i] for i in [1, 2, 3, 4]] if athlete['split'] is not None
                                ]:
                                thing = parse_event_time(str(timed_athlete['split']))
                                seconds -= thing
                            for timed_athlete in [
                                athlete for athlete in [relay[i] for i in [1, 2, 3, 4]] if athlete['split'] is None
                                ]:
                                timed_athlete['split'] = thing / len([
                                athlete for athlete in [relay[i] for i in [1, 2, 3, 4]] if athlete['split'] is None
                                ])
                        for athlete in [relay[i] for i in [1, 2, 3, 4]]:
                            first_last = athlete['name'].split(' ')
                            first = first_last.pop(0)
                            last = ' '.join(first_last)
                            relay_athletes_dict.append({
                                'athlete':{
                                    'first_name': first,
                                    'last_name': last,
                                    'team': team,
                                    'gender': gender,
                                },
                                'result':{
                                    'event': event,
                                    'heat': heat,
                                    'place': place,
                                    'wind': wind,
                                    'team': team,
                                    'points': points / 4,
                                    'meet_date': meet_date,
                                    'result': str(athlete['split']),
                                    'meet': meet_name,
                                    'gender': gender,
                                    'result_metadata': {
                                        'split': True,
                                    }
                                },
                            })
                        break

            result_data = {
                'event': event,
                'heat': heat,
                'place': place,
                'wind': wind,
                'team': team,
                'points': points,
                'meet_date': meet_date,
                'result': result,
                'meet': meet_name,
                'gender': gender,
            }

            data_obj = {
                'athlete': athlete_data,
                'result': result_data,
                'relay_athletes': relay_athletes_dict,
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


def parse_meet_file(path: str, meet_name: str, meet_dates: dict, calendar_year: int, relay_filepath: str):
    with open(path, 'r') as tf:
        data = [l[:-1] for l in tf.readlines()]
    if os.path.exists(relay_filepath):
        with open(relay_filepath, 'r') as yf:
            relay_data = yaml.safe_load(yf)
    else:
        relay_data = {}

    event = None
    header = []
    meet_data = []
    data_row = []
    for _, deets in meet_dates.get(str(calendar_year), {}).items():
        if os.path.basename(path) == deets['filename']:
            meet_metadata = {
                'date': deets['date'],
                'meet_name': deets['meet'],
                'location': deets['location'],
                'small_meet': deets.get('small_meet', False),
            }
            tri_meet = deets.get('small_meet', False)
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
            row = parse_data_row(
                data_row=data_row,
                event=event,
                header=header,
                calendar_year=calendar_year,
                meet_name=meet_name,
                meet_metadata=meet_metadata,
                relay_data=relay_data,
                tri_meet=tri_meet)
            if row:
                meet_data.append(row)
            data_row = []

        if event and header:
            data_row.append(line)

        re_strings = (  # Grabbing event names
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
            'girls? academic',  # There was a national comp with an odd school team name
        )
        if any([re.search(i, line.replace("'", '').strip().lower()) for i in re_strings]) and not any([re.search(i, line.replace("'", '').strip().lower()) for i in re_skip_strings]):
            if data_row:
                data_row.pop(-1)

            row = parse_data_row(
                data_row=data_row,
                event=event,
                header=header,
                calendar_year=calendar_year,
                meet_name=meet_name,
                meet_metadata=meet_metadata,
                relay_data=relay_data,
                tri_meet=tri_meet)
            if row:
                meet_data.append(row)
            data_row = []
            event = line
        if line.strip().lower().startswith(('place')):
            header = [l.strip() for l in line.split(' ')]

    output_data = {}
    for record in meet_data:
        if record['result']['event'] not in output_data:
            output_data[record['result']['event']] = []
        output_data[record['result']['event']].append(record)

    if relay_data['Boys'] or relay_data['Girls']:
        x=1  # Did i get all the relay data?

    for event, results in output_data.items():
        shared_places = []
        lagging_place = [(None, None)]  # (index, place)
        for result_i in range(len(results)):
            result = results[result_i]
            if result['result']['place'] == lagging_place[0][1]:
                # Its a shared place
                lagging_place.append((result_i, result['result']['place']))
            elif len(lagging_place) > 1:
                # Share places
                assigned_points = 0
                for tmp_place in range(len(lagging_place)):
                    assigned_points += assess_points(event=event, place=lagging_place[0][1] + tmp_place, tri_meet=tri_meet)
                assigned_points = round(assigned_points / len(lagging_place), 3)
                for index, place in lagging_place:
                    a = results[index]
                    a_athlete = a['athlete']
                    a_result = a['result']
                    results[index]['result']['points'] = assigned_points
                lagging_place = [(None, None)]
            else:
                # Not a shared place
                lagging_place = [(result_i, result['result']['place'])]
            if result['result']['place'] > 8 and result['result']['points'] == 0:
                break

    return output_data

# Setting up data
meets_dirs = []
for item in os.listdir(etc_dir):
    if item.endswith('_results'):


        x=1
        # REMOVE THIS ITS JUST TO SPEED IT UP TONIGHT
        if '2025' not in item:
            continue
        x=1
        meets_dirs.append(os.path.join(etc_dir, item))

with open(MEET_DATES_PATH, 'r') as jf:
    meet_dates = json.loads(jf.read())

meets_results = {}
for meets in meets_dirs:
    for meet in os.listdir(meets):
        if not meet.endswith('.txt'):
            continue
        meet_filepath = os.path.join(meets, meet)
        relay_filepath = meet_filepath.replace('.txt', ' Relays.yml')
        meet_name = meet.replace('.txt','').strip()
        meet_year = int(meet_filepath.split('/')[-2][5:9])
        x=1
        results = parse_meet_file(path=meet_filepath, meet_name=meet_name, meet_dates=meet_dates, calendar_year=meet_year, relay_filepath=relay_filepath)
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
