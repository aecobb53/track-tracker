from multiprocessing.sharedctypes import Value
import re


class EventParser:
    """
    Parse the event and provide metadata.
    """
    def __init__(self, event: str):
        self.event_s = event
        self.parse_event(event)

    def parse_event(self, event_s: str):
        if re.search(r'(Dash|Run|Relay|Hurdles|Steeplechase|Javelin|Racewalk|Meter)', event_s):
            self.re_s = r'(?P<MINUTES>\d+:)?(?P<SECONDS>\d+)\.?(?P<SUBSECOND>\d*)'
            self.event_type = 'run'
        elif re.search(r'(Shot[\s\t]*Put|Discus|Hammer[\s\t]+Throw|High[\s\t]+Jump|Long[\s\t]+Jump|Triple[\s\t]+Jump|Pole[\s\t]+Vault)', event_s):
            self.re_s = r'((?P<FEET>\d+)-)?(?P<INCHES>\d*)\.?(?P<FRACTIONS>\d*)'
            self.event_type = 'field'
        else:
            raise ValueError(f"UNABLE TO DETERMINE EVENT TYPE FOR {event_s}")

    def parse_gender(self, event_s: str):
        if re.search(r'(Boys?|Mens?)', event_s):
            self.gender = 'Boys'
        elif re.search(r'(Girls?|Womens?)', event_s):
            self.gender = 'Girls'
        else:
            x=1
        return self.gender

    def parse_result(self, result_s: str):
        if not result_s or result_s == '-':
            return None, None, None, None, None, None
        re_s = re.search(self.re_s, result_s)
        if re_s:
            minutes = seconds = subsecond = feet = inches = fractions = None
            try:
                minutes = re_s.group('MINUTES')
            except:
                pass
            try:
                seconds = re_s.group('SECONDS')
            except:
                pass
            try:
                subsecond = re_s.group('SUBSECOND')
            except:
                pass
            try:
                feet = re_s.group('FEET')
            except:
                pass
            try:
                inches = re_s.group('INCHES')
            except:
                pass
            try:
                fractions = re_s.group('FRACTIONS')
            except:
                pass


            if not any([minutes, seconds, subsecond, feet, inches, fractions]):
                raise ValueError(f"Result {result_s} is not valid for event {self.event_s} [{minutes, seconds, subsecond, feet, inches, fractions}]")
            # if not all([seconds, subsecond, subsecond]) and not all([feet, inches, fractions]):
            #     raise ValueError(f"Result {result_s} is not valid for event {self.event_s} [{minutes, seconds, subsecond, feet, inches, fractions}]")
            if minutes is not None:
                minutes = int(minutes[:-1])
            if seconds is not None:
                seconds = int(seconds)
            if subsecond is not None:
                subsecond = float(f"0.{subsecond}")
            if feet is not None:
                feet = int(feet)
            if inches is not None:
                inches = int(inches)
            if fractions is not None:
                fractions = float(f"0.{fractions}")
            return minutes, seconds, subsecond, feet, inches, fractions
        else:
            return None, None, None, None, None, None

    @classmethod
    def parse_event_result(cls, event_s: str, result_s: str):
        ep = cls(event_s)
        result = ep.parse_result(result_s)
        if result is None:
            if ep.event_type == 'run':
                result  = (0, 0, 0, None, None, None)
            elif ep.event_type == 'field':
                result  = (None, None, None, 0, 0, 0)
        return result

    @classmethod
    def parse_event_gender(cls, event_s: str):
        ep = cls(event_s)
        result = ep.parse_gender(event_s)
        return result

# # re_s = re.search(r'(?P<THING>\d+:?\d+\.?\d*)', '1:23.45')

# # a = re_s.groups(0)
# # b = re_s['THING']
# # x=1

# import json
# with open('etc/tmp/BIG_ASS_JSON.json', 'r') as jf:
#     data = json.load(jf)

# events = set()
# for meet, events_d in data.items():
#     for event, entries in events_d.items():
#         events.add(event)
#         for entry in entries:
#             if event == 'raw':
#                 continue
#             ep = EventParser(event)
#             ep.parse_result(entry['result'])
# events_l = list(events)
# events_l.sort()
# for i in events_l:
# x=1

# events_l = [
#     '1A Boys 100 Meter Dash Finals',
#     '1A Boys 110 Meter Hurdles Finals',
#     '1A Boys 1600 Meter Run Finals',
#     '1A Boys 200 Meter Dash Finals',
#     '1A Boys 300 Meter Hurdles Finals',
#     '1A Boys 3200 Meter Run Finals',
#     '1A Boys 400 Meter Dash Finals',
#     '1A Boys 4x100 Meter Relay Finals',
#     '1A Boys 4x200 Meter Relay Finals',
#     '1A Boys 4x400 Meter Relay Finals',
#     '1A Boys 4x800 Meter Relay Finals',
#     '1A Boys 800 Meter Run Finals',
#     '1A Boys Discus Finals',
#     '1A Boys High Jump Finals',
#     '1A Boys Long Jump Finals',
#     '1A Boys Pole Vault Finals',
#     '1A Boys Shot Put Finals',
#     '1A Boys Triple Jump Finals',
#     '1A Girls 100 Meter Dash Finals',
#     '1A Girls 100 Meter Hurdles Finals',
#     '1A Girls 1600 Meter Run Finals',
#     '1A Girls 200 Meter Dash Finals',
#     '1A Girls 300 Meter Hurdles Finals',
#     '1A Girls 3200 Meter Run Finals',
#     '1A Girls 400 Meter Dash Finals',
#     '1A Girls 4x100 Meter Relay Finals',
#     '1A Girls 4x200 Meter Relay Finals',
#     '1A Girls 4x400 Meter Relay Finals',
#     '1A Girls 4x800 Meter Relay Finals',
#     '1A Girls 800 Meter Run Finals',
#     '1A Girls Discus Finals',
#     '1A Girls High Jump Finals',
#     '1A Girls Long Jump Finals',
#     '1A Girls Pole Vault Finals',
#     '1A Girls Shot Put Finals',
#     '1A Girls Triple Jump Finals',
#     '2A Boys 100 Meter Dash Finals',
#     '2A Boys 100 Meter Dash Prelims',
#     '2A Boys 110 Meter Hurdles Finals',
#     '2A Boys 110 Meter Hurdles Prelims',
#     '2A Boys 1600 Meter Run Finals',
#     '2A Boys 200 Meter Dash Finals',
#     '2A Boys 200 Meter Dash Prelims',
#     '2A Boys 300 Meter Hurdles Finals',
#     '2A Boys 300 Meter Hurdles Prelims',
#     '2A Boys 3200 Meter Run Finals',
#     '2A Boys 400 Meter Dash Finals',
#     '2A Boys 400 Meter Dash Prelims',
#     '2A Boys 4x100 Meter Relay Finals',
#     '2A Boys 4x100 Meter Relay Prelims',
#     '2A Boys 4x200 Meter Relay Finals',
#     '2A Boys 4x400 Meter Relay Finals',
#     '2A Boys 4x400 Meter Relay Prelims',
#     '2A Boys 800 Meter Run Finals',
#     '2A Boys Discus Finals',
#     '2A Boys High Jump Finals',
#     '2A Boys Long Jump Finals',
#     '2A Boys Pole Vault Finals',
#     '2A Boys Shot Put Finals',
#     '2A Boys Triple Jump Finals',
#     '2A Girls 100 Meter Dash Finals',
#     '2A Girls 100 Meter Dash Prelims',
#     '2A Girls 100 Meter Hurdles Finals',
#     '2A Girls 100 Meter Hurdles Prelims',
#     '2A Girls 1600 Meter Run Finals',
#     '2A Girls 200 Meter Dash Finals',
#     '2A Girls 200 Meter Dash Prelims',
#     '2A Girls 300 Meter Hurdles Finals',
#     '2A Girls 300 Meter Hurdles Prelims',
#     '2A Girls 3200 Meter Run Finals',
#     '2A Girls 400 Meter Dash Finals',
#     '2A Girls 400 Meter Dash Prelims',
#     '2A Girls 4x100 Meter Relay Finals',
#     '2A Girls 4x100 Meter Relay Prelims',
#     '2A Girls 4x200 Meter Relay Finals',
#     '2A Girls 4x400 Meter Relay Finals',
#     '2A Girls 4x400 Meter Relay Prelims',
#     '2A Girls 800 Meter Run Finals',
#     '2A Girls 800 Meter Sprint Medley Relay Finals',
#     '2A Girls Discus Finals',
#     '2A Girls High Jump Finals',
#     '2A Girls Long Jump Finals',
#     '2A Girls Pole Vault Finals',
#     '2A Girls Shot Put Finals',
#     '2A Girls Triple Jump Finals',
#     '3A Boys 100 Meter Dash Finals',
#     '3A Boys 100 Meter Dash Prelims',
#     '3A Boys 110 Meter Hurdles Finals',
#     '3A Boys 110 Meter Hurdles Prelims',
#     '3A Boys 1600 Meter Run Finals',
#     '3A Boys 200 Meter Dash Finals',
#     '3A Boys 200 Meter Dash Prelims',
#     '3A Boys 300 Meter Hurdles Finals',
#     '3A Boys 300 Meter Hurdles Prelims',
#     '3A Boys 3200 Meter Run Finals',
#     '3A Boys 400 Meter Dash Finals',
#     '3A Boys 400 Meter Dash Prelims',
#     '3A Boys 4x100 Meter Relay Finals',
#     '3A Boys 4x100 Meter Relay Prelims',
#     '3A Boys 4x200 Meter Relay Finals',
#     '3A Boys 4x400 Meter Relay Finals',
#     '3A Boys 4x400 Meter Relay Prelims',
#     '3A Boys 800 Meter Run Finals',
#     '3A Boys Discus Finals',
#     '3A Boys High Jump Finals',
#     '3A Boys Long Jump Finals',
#     '3A Boys Pole Vault Finals',
#     '3A Boys Shot Put Finals',
#     '3A Boys Triple Jump Finals',
#     '3A Girls 100 Meter Dash Finals',
#     '3A Girls 100 Meter Dash Prelims',
#     '3A Girls 100 Meter Hurdles Finals',
#     '3A Girls 100 Meter Hurdles Prelims',
#     '3A Girls 1600 Meter Run Finals',
#     '3A Girls 200 Meter Dash Finals',
#     '3A Girls 200 Meter Dash Prelims',
#     '3A Girls 300 Meter Hurdles Finals',
#     '3A Girls 300 Meter Hurdles Prelims',
#     '3A Girls 3200 Meter Run Finals',
#     '3A Girls 400 Meter Dash Finals',
#     '3A Girls 400 Meter Dash Prelims',
#     '3A Girls 4x100 Meter Relay Finals',
#     '3A Girls 4x100 Meter Relay Prelims',
#     '3A Girls 4x200 Meter Relay Finals',
#     '3A Girls 4x400 Meter Relay Finals',
#     '3A Girls 4x400 Meter Relay Prelims',
#     '3A Girls 800 Meter Run Finals',
#     '3A Girls 800 Meter Sprint Medley Relay Finals',
#     '3A Girls Discus Finals',
#     '3A Girls High Jump Finals',
#     '3A Girls Long Jump Finals',
#     '3A Girls Pole Vault Finals',
#     '3A Girls Shot Put Finals',
#     '3A Girls Triple Jump Finals',
#     '4A Boys 100 Meter Dash Finals',
#     '4A Boys 100 Meter Dash Prelims',
#     '4A Boys 110 Meter Hurdles Finals',
#     '4A Boys 110 Meter Hurdles Prelims',
#     '4A Boys 1600 Meter Run Finals',
#     '4A Boys 200 Meter Dash Finals',
#     '4A Boys 200 Meter Dash Prelims',
#     '4A Boys 300 Meter Hurdles Finals',
#     '4A Boys 300 Meter Hurdles Prelims',
#     '4A Boys 3200 Meter Run Finals',
#     '4A Boys 400 Meter Dash Finals',
#     '4A Boys 400 Meter Dash Prelims',
#     '4A Boys 4x100 Meter Relay Finals',
#     '4A Boys 4x100 Meter Relay Prelims',
#     '4A Boys 4x200 Meter Relay Finals',
#     '4A Boys 4x400 Meter Relay Finals',
#     '4A Boys 4x400 Meter Relay Prelims',
#     '4A Boys 800 Meter Run Finals',
#     '4A Boys Discus Finals',
#     '4A Boys High Jump Finals',
#     '4A Boys Long Jump Finals',
#     '4A Boys Pole Vault Finals',
#     '4A Boys Shot Put Finals',
#     '4A Boys Triple Jump Finals',
#     '4A Girls 100 Meter Dash Finals',
#     '4A Girls 100 Meter Dash Prelims',
#     '4A Girls 100 Meter Hurdles Finals',
#     '4A Girls 100 Meter Hurdles Prelims',
#     '4A Girls 1600 Meter Run Finals',
#     '4A Girls 200 Meter Dash Finals',
#     '4A Girls 200 Meter Dash Prelims',
#     '4A Girls 300 Meter Hurdles Finals',
#     '4A Girls 300 Meter Hurdles Prelims',
#     '4A Girls 3200 Meter Run Finals',
#     '4A Girls 400 Meter Dash Finals',
#     '4A Girls 400 Meter Dash Prelims',
#     '4A Girls 4x100 Meter Relay Finals',
#     '4A Girls 4x100 Meter Relay Prelims',
#     '4A Girls 4x200 Meter Relay Finals',
#     '4A Girls 4x400 Meter Relay Finals',
#     '4A Girls 4x400 Meter Relay Prelims',
#     '4A Girls 800 Meter Run Finals',
#     '4A Girls 800 Meter Sprint Medley Relay Finals',
#     '4A Girls Discus Finals',
#     '4A Girls High Jump Finals',
#     '4A Girls Long Jump Finals',
#     '4A Girls Pole Vault Finals',
#     '4A Girls Shot Put Finals',
#     '4A Girls Triple Jump Finals',
#     '5A Boys 100 Meter Dash Finals',
#     '5A Boys 100 Meter Dash Prelims',
#     '5A Boys 110 Meter Hurdles Finals',
#     '5A Boys 110 Meter Hurdles Prelims',
#     '5A Boys 1600 Meter Run Finals',
#     '5A Boys 200 Meter Dash Finals',
#     '5A Boys 200 Meter Dash Prelims',
#     '5A Boys 300 Meter Hurdles Finals',
#     '5A Boys 300 Meter Hurdles Prelims',
#     '5A Boys 3200 Meter Run Finals',
#     '5A Boys 400 Meter Dash Finals',
#     '5A Boys 400 Meter Dash Prelims',
#     '5A Boys 4x100 Meter Relay Finals',
#     '5A Boys 4x100 Meter Relay Prelims',
#     '5A Boys 4x200 Meter Relay Finals',
#     '5A Boys 4x400 Meter Relay Finals',
#     '5A Boys 4x400 Meter Relay Prelims',
#     '5A Boys 800 Meter Run Finals',
#     '5A Boys Discus Finals',
#     '5A Boys High Jump Finals',
#     '5A Boys Long Jump Finals',
#     '5A Boys Pole Vault Finals',
#     '5A Boys Shot Put Finals',
#     '5A Boys Triple Jump Finals',
#     '5A Girls 100 Meter Dash Finals',
#     '5A Girls 100 Meter Dash Prelims',
#     '5A Girls 100 Meter Hurdles Finals',
#     '5A Girls 100 Meter Hurdles Prelims',
#     '5A Girls 1600 Meter Run Finals',
#     '5A Girls 200 Meter Dash Finals',
#     '5A Girls 200 Meter Dash Prelims',
#     '5A Girls 300 Meter Hurdles Finals',
#     '5A Girls 300 Meter Hurdles Prelims',
#     '5A Girls 3200 Meter Run Finals',
#     '5A Girls 400 Meter Dash Finals',
#     '5A Girls 400 Meter Dash Prelims',
#     '5A Girls 4x100 Meter Relay Finals',
#     '5A Girls 4x100 Meter Relay Prelims',
#     '5A Girls 4x200 Meter Relay Finals',
#     '5A Girls 4x400 Meter Relay Finals',
#     '5A Girls 4x400 Meter Relay Prelims',
#     '5A Girls 800 Meter Run Finals',
#     '5A Girls 800 Meter Sprint Medley Relay Finals',
#     '5A Girls Discus Finals',
#     '5A Girls High Jump Finals',
#     '5A Girls Long Jump Finals',
#     '5A Girls Pole Vault Finals',
#     '5A Girls Shot Put Finals',
#     '5A Girls Triple Jump Finals',
#     'Boys 100 Meter Dash Finals',
#     'Boys 100 Meter Dash Prelims',
#     'Boys 100 Meter Wheelchair Race Finals',
#     'Boys 110 Meter Hurdles Finals',
#     'Boys 110 Meter Hurdles Prelims',
#     'Boys 1600 Meter Run Finals',
#     'Boys 200 Meter Dash Finals',
#     'Boys 200 Meter Dash Prelims',
#     'Boys 200 Meter Wheelchair Race Finals',
#     'Boys 2000 Meter Steeplechase Finals',
#     'Boys 300 Meter Hurdles Finals',
#     'Boys 300 Meter Hurdles Prelims',
#     'Boys 3200 Meter Run Finals',
#     'Boys 400 Meter Dash Finals',
#     'Boys 400 Meter Dash Prelims',
#     'Boys 4x100 Meter Relay Finals',
#     'Boys 4x100 Meter Throwers Relay Finals',
#     'Boys 4x110 Shuttle Hurdle Relay Finals',
#     'Boys 4x1600 Meter Relay Finals',
#     'Boys 4x200 Meter Relay Finals',
#     'Boys 4x400 Meter Relay Finals',
#     'Boys 4x800 Meter Relay Finals',
#     'Boys 4xMile Relay Finals',
#     'Boys 800 Meter Run Finals',
#     'Boys 800 Meter Sprint Medley Relay Finals',
#     'Boys Discus Finals',
#     'Boys Distance Medley Relay Finals',
#     'Boys High Jump Finals',
#     'Boys Javelin Finals',
#     'Boys Long Jump Finals',
#     'Boys One Mile Run Finals',
#     'Boys Pole Vault Finals',
#     'Boys Shot Put Finals',
#     'Boys Sprint Medley Relay Finals',
#     'Boys Triple Jump Finals',
#     'Boys Wheelchair Discus Finals',
#     'Boys Wheelchair Shot Put Finals',
#     'Championship Boys 100 Meter Dash Finals',
#     'Championship Boys 100 Meter Dash Prelims',
#     'Championship Boys 100 Meter Dash X',
#     'Championship Boys 110 Meter Hurdles Finals',
#     'Championship Boys 110 Meter Hurdles Prelims',
#     'Championship Boys 1500 Meter Run Finals',
#     'Championship Boys 2 Mile Run Finals',
#     'Championship Boys 200 Meter Dash Finals',
#     'Championship Boys 200 Meter Dash Prelims',
#     'Championship Boys 2000 Meter Steeplechase Finals',
#     'Championship Boys 3000 Meter Racewalk Finals',
#     'Championship Boys 3000 Meter Run Finals',
#     'Championship Boys 400 Meter Dash Finals',
#     'Championship Boys 400 Meter Dash X',
#     'Championship Boys 400 Meter Hurdles Finals',
#     'Championship Boys 4x100 Meter Relay Prelims',
#     'Championship Boys 4x200 Meter Relay Finals',
#     'Championship Boys 4x400 Meter Relay Finals',
#     'Championship Boys 4x800 Meter Relay Finals',
#     'Championship Boys 5000 Meter Run Finals',
#     'Championship Boys 800 Meter Run Finals',
#     'Championship Boys Discus Finals',
#     'Championship Boys Distance Medley Relay Finals',
#     'Championship Boys Hammer Throw Finals',
#     'Championship Boys High Jump Finals',
#     'Championship Boys High Jump X',
#     'Championship Boys Javelin Finals',
#     'Championship Boys Long Jump Finals',
#     'Championship Boys Long Jump X',
#     'Championship Boys One Mile Run Finals',
#     'Championship Boys Pole Vault Finals',
#     'Championship Boys Shot Put Finals',
#     'Championship Boys Shot Put X',
#     'Championship Boys Sprint Medley Relay Finals',
#     'Championship Boys Triple Jump Finals',
#     'Championship Girls 100 Meter Dash Finals',
#     'Championship Girls 100 Meter Dash Prelims',
#     'Championship Girls 100 Meter Hurdles Finals',
#     'Championship Girls 100 Meter Hurdles Prelims',
#     'Championship Girls 2 Mile Run Finals',
#     'Championship Girls 200 Meter Dash Finals',
#     'Championship Girls 200 Meter Dash Prelims',
#     'Championship Girls 2000 Meter Steeplechase Finals',
#     'Championship Girls 3000 Meter Racewalk Finals',
#     'Championship Girls 3000 Meter Run Finals',
#     'Championship Girls 400 Meter Dash Finals',
#     'Championship Girls 400 Meter Hurdles Finals',
#     'Championship Girls 4x100 Meter Relay Prelims',
#     'Championship Girls 4x200 Meter Relay Finals',
#     'Championship Girls 4x400 Meter Relay Finals',
#     'Championship Girls 4x800 Meter Relay Finals',
#     'Championship Girls 4xMile Relay Finals',
#     'Championship Girls 5000 Meter Run Finals',
#     'Championship Girls 800 Meter Run Finals',
#     'Championship Girls Discus Finals',
#     'Championship Girls Distance Medley Relay Finals',
#     'Championship Girls Hammer Throw Finals',
#     'Championship Girls High Jump Finals',
#     'Championship Girls Javelin Finals',
#     'Championship Girls Javelin X',
#     'Championship Girls Long Jump Finals',
#     'Championship Girls Long Jump X',
#     'Championship Girls One Mile Run Finals',
#     'Championship Girls Pole Vault Finals',
#     'Championship Girls Shot Put Finals',
#     'Championship Girls Sprint Medley Relay Finals',
#     'Championship Girls Triple Jump Finals',
#     'Club Girls 4x400 Meter Relay Finals',
#     'Club Girls Distance Medley Relay Finals',
#     'Emerging Elite Boys 100 Meter Dash Finals',
#     'Emerging Elite Boys 100 Meter Dash Prelims',
#     'Emerging Elite Boys 110 Meter Hurdles Finals',
#     'Emerging Elite Boys 110 Meter Hurdles Prelims',
#     'Emerging Elite Boys 2 Mile Run Finals',
#     'Emerging Elite Boys 200 Meter Dash Finals',
#     'Emerging Elite Boys 200 Meter Dash Prelims',
#     'Emerging Elite Boys 3000 Meter Run Finals',
#     'Emerging Elite Boys 400 Meter Dash Finals',
#     'Emerging Elite Boys 400 Meter Hurdles Finals',
#     'Emerging Elite Boys 4x100 Meter Relay Finals',
#     'Emerging Elite Boys 4x100 Meter Relay Prelims',
#     'Emerging Elite Boys 4x200 Meter Relay Finals',
#     'Emerging Elite Boys 4x400 Meter Relay Finals',
#     'Emerging Elite Boys 4x800 Meter Relay Finals',
#     'Emerging Elite Boys 800 Meter Run Finals',
#     'Emerging Elite Boys Discus Finals',
#     'Emerging Elite Boys Hammer Throw Finals',
#     'Emerging Elite Boys High Jump Finals',
#     'Emerging Elite Boys Javelin Finals',
#     'Emerging Elite Boys Long Jump Finals',
#     'Emerging Elite Boys One Mile Run Finals',
#     'Emerging Elite Boys Pole Vault Finals',
#     'Emerging Elite Boys Shot Put Finals',
#     'Emerging Elite Boys Sprint Medley Relay Finals',
#     'Emerging Elite Boys Triple Jump Finals',
#     'Emerging Elite Girls 100 Meter Dash Finals',
#     'Emerging Elite Girls 100 Meter Dash Prelims',
#     'Emerging Elite Girls 100 Meter Hurdles Finals',
#     'Emerging Elite Girls 100 Meter Hurdles Prelims',
#     'Emerging Elite Girls 2 Mile Run Finals',
#     'Emerging Elite Girls 200 Meter Dash Finals',
#     'Emerging Elite Girls 200 Meter Dash Prelims',
#     'Emerging Elite Girls 3000 Meter Run Finals',
#     'Emerging Elite Girls 400 Meter Dash Finals',
#     'Emerging Elite Girls 400 Meter Hurdles Finals',
#     'Emerging Elite Girls 4x100 Meter Relay Finals',
#     'Emerging Elite Girls 4x100 Meter Relay Prelims',
#     'Emerging Elite Girls 4x200 Meter Relay Finals',
#     'Emerging Elite Girls 4x400 Meter Relay Finals',
#     'Emerging Elite Girls 4x800 Meter Relay Finals',
#     'Emerging Elite Girls 800 Meter Run Finals',
#     'Emerging Elite Girls Discus Finals',
#     'Emerging Elite Girls Hammer Throw Finals',
#     'Emerging Elite Girls High Jump Finals',
#     'Emerging Elite Girls Javelin Finals',
#     'Emerging Elite Girls Long Jump Finals',
#     'Emerging Elite Girls One Mile Run Finals',
#     'Emerging Elite Girls Pole Vault Finals',
#     'Emerging Elite Girls Shot Put Finals',
#     'Emerging Elite Girls Sprint Medley Relay Finals',
#     'Emerging Elite Girls Triple Jump Finals',
#     'Freshman Boys 100 Meter Dash Finals',
#     'Freshman Boys 100 Meter Dash Prelims',
#     'Freshman Boys 1500 Meter Run Finals',
#     'Freshman Boys One Mile Run Finals',
#     'Freshman Girls 100 Meter Dash Finals',
#     'Freshman Girls 100 Meter Dash Prelims',
#     'Freshman Girls 1500 Meter Run Finals',
#     'Freshman Girls 1600 Meter Run Finals',
#     'Freshman Girls One Mile Run Finals',
#     'Girls 100 Meter Dash Finals',
#     'Girls 100 Meter Dash Prelims',
#     'Girls 100 Meter Hurdles Finals',
#     'Girls 100 Meter Hurdles Prelims',
#     'Girls 100 Meter Wheelchair Race Finals',
#     'Girls 1600 Meter Run Finals',
#     'Girls 200 Meter Dash Finals',
#     'Girls 200 Meter Dash Prelims',
#     'Girls 200 Meter Wheelchair Race Finals',
#     'Girls 2000 Meter Steeplechase Finals',
#     'Girls 300 Meter Hurdles Finals',
#     'Girls 300 Meter Hurdles Prelims',
#     'Girls 3000 Meter Run Finals',
#     'Girls 3200 Meter Run Finals',
#     'Girls 400 Meter Dash Finals',
#     'Girls 400 Meter Dash Prelims',
#     'Girls 4x100 Meter Relay Finals',
#     'Girls 4x100 Shuttle Hurdle Relay Finals',
#     'Girls 4x1600 Meter Relay Finals',
#     'Girls 4x200 Meter Relay Finals',
#     'Girls 4x400 Meter Relay Finals',
#     'Girls 4x800 Meter Relay Finals',
#     'Girls 800 Meter Run Finals',
#     'Girls 800 Meter Sprint Medley Relay Finals',
#     'Girls Discus Finals',
#     'Girls Distance Medley Relay Finals',
#     'Girls High Jump Finals',
#     'Girls Javelin Finals',
#     'Girls Long Jump Finals',
#     'Girls One Mile Run Finals',
#     'Girls Pole Vault Finals',
#     'Girls Shot Put Finals',
#     'Girls Sprint Medley Relay Finals',
#     'Girls Triple Jump Finals',
#     'Girls Wheelchair Shot Put Finals',
#     'Mens 100 Meter Dash Finals',
#     'Mens 110 Meter Hurdles Finals',
#     'Mens 1600 Meter Run Finals',
#     'Mens 200 Meter Dash Finals',
#     'Mens 300 Meter Hurdles Finals',
#     'Mens 3200 Meter Run Finals',
#     'Mens 400 Meter Dash Finals',
#     'Mens 4x100 Meter Relay Finals',
#     'Mens 4x200 Meter Relay Finals',
#     'Mens 4x400 Meter Relay Finals',
#     'Mens 4x800 Meter Relay Finals',
#     'Mens 800 Meter Run Finals',
#     'Mens High Jump Finals',
#     'Mens Long Jump Finals',
#     'Mens Pole Vault Finals',
#     'Mens Triple Jump Finals',
#     'Middle School Boys 100 Meter Dash Finals',
#     'Middle School Boys 100 Meter Dash Prelims',
#     'Middle School Boys 1500 Meter Run Finals',
#     'Middle School Boys 200 Meter Dash Finals',
#     'Middle School Boys 400 Meter Dash Finals',
#     'Middle School Boys 800 Meter Run Finals',
#     'Middle School Boys Long Jump Finals',
#     'Middle School Boys One Mile Run Finals',
#     'Middle School Boys Shot Put Finals',
#     'Middle School Girls 100 Meter Dash Finals',
#     'Middle School Girls 100 Meter Dash Prelims',
#     'Middle School Girls 1500 Meter Run Finals',
#     'Middle School Girls 200 Meter Dash Finals',
#     'Middle School Girls 400 Meter Dash Finals',
#     'Middle School Girls 800 Meter Run Finals',
#     'Middle School Girls Long Jump Finals',
#     'Middle School Girls One Mile Run Finals',
#     'Middle School Girls Shot Put Finals',
#     'Pro Boys 1500 Meter Run Finals',
#     'Varsity Boys 100 Meter Dash Finals',
#     'Varsity Boys 110 Meter Hurdles Finals',
#     'Varsity Boys 1600 Meter Run Finals',
#     'Varsity Boys 200 Meter Dash Finals',
#     'Varsity Boys 300 Meter Hurdles Finals',
#     'Varsity Boys 3200 Meter Run Finals',
#     'Varsity Boys 400 Meter Dash Finals',
#     'Varsity Boys 4x100 Meter Relay Finals',
#     'Varsity Boys 4x200 Meter Relay Finals',
#     'Varsity Boys 4x400 Meter Relay Finals',
#     'Varsity Boys 4x800 Meter Relay Finals',
#     'Varsity Boys 800 Meter Run Finals',
#     'Varsity Boys Discus Finals',
#     'Varsity Boys High Jump Finals',
#     'Varsity Boys Long Jump Finals',
#     'Varsity Boys Pole Vault Finals',
#     'Varsity Boys Shot Put Finals',
#     'Varsity Boys Triple Jump Finals',
#     'Varsity Girls 100 Meter Dash Finals',
#     'Varsity Girls 100 Meter Hurdles Finals',
#     'Varsity Girls 1600 Meter Run Finals',
#     'Varsity Girls 200 Meter Dash Finals',
#     'Varsity Girls 300 Meter Hurdles Finals',
#     'Varsity Girls 3200 Meter Run Finals',
#     'Varsity Girls 400 Meter Dash Finals',
#     'Varsity Girls 4x100 Meter Relay Finals',
#     'Varsity Girls 4x200 Meter Relay Finals',
#     'Varsity Girls 4x400 Meter Relay Finals',
#     'Varsity Girls 4x800 Meter Relay Finals',
#     'Varsity Girls 800 Meter Run Finals',
#     'Varsity Girls 800 Meter Sprint Medley Relay Finals',
#     'Varsity Girls Discus Finals',
#     'Varsity Girls High Jump Finals',
#     'Varsity Girls Long Jump Finals',
#     'Varsity Girls Pole Vault Finals',
#     'Varsity Girls Shot Put Finals',
#     'Varsity Girls Triple Jump Finals',
#     'Womens 100 Meter Dash Finals',
#     'Womens 100 Meter Hurdles Finals',
#     'Womens 1600 Meter Run Finals',
#     'Womens 200 Meter Dash Finals',
#     'Womens 300 Meter Hurdles Finals',
#     'Womens 3200 Meter Run Finals',
#     'Womens 400 Meter Dash Finals',
#     'Womens 4x100 Meter Relay Finals',
#     'Womens 4x200 Meter Relay Finals',
#     'Womens 4x400 Meter Relay Finals',
#     'Womens 4x800 Meter Relay Finals',
#     'Womens 800 Meter Run Finals',
#     'Womens Discus Finals',
#     'Womens High Jump Finals',
#     'Womens Long Jump Finals',
#     'Womens Pole Vault Finals',
#     'Womens Shot Put Finals',
#     'Womens Triple Jump Finals',
# ]

# for i in events_l:
#     event = EventParser(i)


