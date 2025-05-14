
import enum
import json
from operator import is_
import os

from datetime import datetime, date, time, timedelta
from enum import Enum
from re import L

from .result import Result, ResultData, ResultApiCreate
from .ms_athlete import AthleteData, AthleteApiCreate
from .event import EventParser


class BespokeDataObjectBase:
    def __init__(self, *args, **kwargs):
        pass


class UpdateType(Enum):
    ADD = 'add'
    UPDATE = 'update'
    DELETE = 'delete'


class BespokeUpdateObjectBase:
    def __init__(self, *args, **kwargs):
        self.update_types = set()

    def add_update_type(self, update_type: UpdateType):
        self.update_types.add(update_type)


class EventType:
    def __init__(self,
        running: bool,
        field: bool,
        sprint: bool,
        distance: bool,
        throws: bool,
        jumps: bool,
        relay: bool,
        ):
        self.running = running
        self.field = field
        self.sprint = sprint
        self.distance = distance
        self.throws = throws
        self.jumps = jumps
        self.relay = relay

    def __eq__(self, other_object: object) -> bool:
        if self.running != other_object.running:
            return False
        if self.field != other_object.field:
            return False
        if self.sprint != other_object.sprint:
            return False
        if self.distance != other_object.distance:
            return False
        if self.throws != other_object.throws:
            return False
        if self.jumps != other_object.jumps:
            return False
        if self.relay != other_object.relay:
            return False
        return True

    @classmethod
    def from_event_type_name(cls, event_type_name: str):
        obj = cls(
            running=False,
            field=False,
            sprint=False,
            distance=False,
            throws=False,
            jumps=False,
            relay=False,
        )
        return obj


class ResultDataObject(BespokeDataObjectBase):
    def __init__(self,
        athlete: AthleteData,
        seed: ResultData | None = None,
        result: ResultData | None = None,
        # team: str,
        heat_lane_flight: str = 'Unknown',
        place: int | None = None,
        is_pr: bool | None = None,
        points: int | None = None,
        *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.athlete = athlete
        self.seed = seed
        self.result = result
        self.heat_lane_flight = heat_lane_flight
        self.place = place
        self.is_pr = is_pr
        self.points = points

    def __repr__(self):
        return f"ResultDataObject(athlete='{self.athlete.name}', result='{self.result.format if self.result else None}', place={self.place})"

    def __str__(self):
        return f"ResultDataObject(athlete='{self.athlete.name}', result='{self.result.format if self.result else None}', place={self.place})"

    def __eq__(self, other_object: object) -> bool:
        if self.athlete != other_object.athlete:
            return False
        if self.seed != other_object.seed:
            return False
        if self.result != other_object.result:
            return False
        if self.heat_lane_flight != other_object.heat_lane_flight:
            return False
        if self.place != other_object.place:
            return False
        if self.is_pr != other_object.is_pr:
            return False
        if self.points != other_object.points:
            return False
        return True

    def update(self, other_result):
        result_update_object = ResultUpdateObject()
        if self.athlete != other_result.athlete:
            result_update_object.add_update('athlete', other_result.athlete)
            self.athlete = other_result.athlete
        if self.seed != other_result.seed:
            result_update_object.add_update('seed', other_result.seed)
            self.seed = other_result.seed
        if self.result != other_result.result:
            result_update_object.add_update('result', other_result.result)
            self.result = other_result.result
        if self.heat_lane_flight != other_result.heat_lane_flight:
            result_update_object.add_update('heat_lane_flight', other_result.heat_lane_flight)
            self.heat_lane_flight = other_result.heat_lane_flight
        if self.place != other_result.place:
            result_update_object.add_update('place', other_result.place)
            self.place = other_result.place
        if self.is_pr != other_result.is_pr:
            result_update_object.add_update('is_pr', other_result.is_pr)
            self.is_pr = other_result.is_pr
        if self.points != other_result.points:
            result_update_object.add_update('points', other_result.points)
            self.points = other_result.points

        if result_update_object:
            return result_update_object
        else:
            return None

    @classmethod
    def import_json(cls, json_data: str | dict, event_data: str | dict | None = None):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data

        if isinstance(event_data, str):
            event_data = json.loads(event_data)
        elif isinstance(event_data, dict):
            event_data = event_data
        """
        THIS WILL NEED TO BE UPDAT4ED BEFORE ADDING TO SERVICE
        """
        first_last = json_data.get('name', '-').split(' ')
        first_name = first_last.pop(0)
        last_name = ' '.join(first_last)
        team = json_data.get('team', 'Fairview High School')
        athlete = AthleteApiCreate(
            first_name=first_name,
            last_name=last_name,
            team=team,
        ).cast_data_object()


        if data.get('seed'):
            seed = Result.parse_event_result(event=event_data['Event'], result=str(data['seed']))
        else:
            seed = None
        if data.get('result'):
            result = Result.parse_event_result(event=event_data['Event'], result=str(data['result']))
        else:
            result = None
        heat_lane_flight = data.get('Heat/Lane/Flight', 'Unknown')
        place = data.get('place', None)
        is_pr = data.get('pr', None)
        points = data.get('points', None)
        # athlete_uid
        # result_uid
        # pr_uid
        # seed_uid

        obj = cls(
            athlete=athlete,
            seed=seed,
            result=result,
            heat_lane_flight=heat_lane_flight,
            place=place,
            is_pr=is_pr,
            points=points,
        )
        return obj

    def export_json(self):
        output = {
            'name': self.athlete.name,
            'seed': self.seed.format if self.seed else None,
            'result': self.result.format if self.result else None,
            'Heat/Lane/Flight': self.heat_lane_flight,
            'place': self.place,
            'pr': self.is_pr,
            'points': self.points,
        }
        return output


class EventDataObject(BespokeDataObjectBase):
    def __init__(self,
        event_name: str,
        event_time: time,
        event_type: EventType,
        is_relay: bool = False,
        *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_name = event_name
        self.event_time = event_time
        self.event_type = event_type
        self.is_relay = is_relay

        self.results = []
        self.team_team_results = {}

    def __iter__(self):
        return iter(self.results)

    def __repr__(self):
        return f"EventDataObject(event_name='{self.event_name}', event_time='{self.event_time}', results_len={len(self.results)})"

    def __str__(self):
        return f"EventDataObject(event_name='{self.event_name}', event_time='{self.event_time}', results_len={len(self.results)})"

    def __eq__(self, other_object: object) -> bool:
        if self.event_name != other_object.event_name:
            return False
        if self.event_time != other_object.event_time:
            return False
        if self.event_type != other_object.event_type:
            return False
        if self.is_relay != other_object.is_relay:
            return False

        if len(self.results) != len(other_object.results):
            return False
        for self_result, other_result in zip(self.results, other_object.results):
            if self_result != other_result:
                return False
        return True

    def add_result(self, result: str, index: int | None = None):
        if index is not None:
            self.results.insert(index, result)
        else:
            self.results.append(result)

    def find_result(self, identifier: str | int) -> ResultDataObject | None:
        if isinstance(identifier, str):
            for result in self.results:
                if result.athlete.name == identifier:
                    return result
            else:
                raise IndexError(f"ResultDataObject with name {identifier} not found.")
        elif isinstance(identifier, int):
            try:
                return self.results[identifier]
            except IndexError:
                return None
        return None

    def remove_result(self, identifier: str | int):
        if isinstance(identifier, str):
            for result in self.results:
                if result.athlete.name == identifier:
                    self.results.remove(result)
                    return
            else:
                raise IndexError(f"ResultDataObject with name {identifier} not found.")
        elif isinstance(identifier, int):
            self.results.pop(identifier)
            return

    def add_team_result(self, team: str, result, index: int | None = None):
        if result.athlete.team not in self.team_team_results:
            self.team_team_results[result.athlete.team] = {}
        if team not in self.team_team_results[result.athlete.team]:
            self.team_team_results[result.athlete.team][team] = []
        if index is not None:
            self.team_team_results[result.athlete.team][team].insert(index, result)
        else:
            self.team_team_results[result.athlete.team][team].append(result)

    def convert_to_relay(self):
        """
        Grabs existing teams and tries to add any results/athletes that slipped through the cracks
        """
        self.is_relay = True
        teams = {k: v for k, v in self.team_team_results.items()}
        for result in self.results:
            if result.athlete.team not in teams:
                teams[result.athlete.team] = {'Team 1': []}
            team_pointer_int = 1
            while True:
                if result.athlete.name.startswith('Team'):
                    break
                team_name = f"Team {team_pointer_int}"
                if team_name not in teams[result.athlete.team]:
                    teams[result.athlete.team][team_name] = []
                if len(teams[result.athlete.team][team_name]) < 4:
                    print(f"RESULT: {result}")
                    results_check = []
                    [results_check.extend(v) for k, v in teams[result.athlete.team].items()]
                    if result in results_check:
                        break
                    teams[result.athlete.team][team_name].append(result)
                    break
                else:
                    team_pointer_int += 1
        self.team_team_results = teams
        self.results = []

    def convert_to_open(self):
        self.is_relay = False
        results = [r for r in self.results]
        for team_results in self.team_team_results.values():
            for team_results_list in team_results.values():
                for result in team_results_list:
                    if result not in results:
                        results.append(result)
        self.results = results
        self.team_team_results = {}

    def update(self, other_event):
        event_update_object = EventUpdateObject()
        if self.event_name != other_event.event_name:
            event_update_object.add_update('event_name', other_event.event_name)
            self.event_name = other_event.event_name
        if self.event_time != other_event.event_time:
            event_update_object.add_update('event_time', other_event.event_time)
            self.event_time = other_event.event_time
        if self.event_type != other_event.event_type:
            event_update_object.add_update('event_type', other_event.event_type)
            self.event_type = other_event.event_type
        if self.is_relay != other_event.is_relay:
            event_update_object.add_update('is_relay', other_event.is_relay)
            self.is_relay = other_event.is_relay

        # Deletion detection
        if len(self.results) > len(other_event.results):
            deleted = []
            for self_index, self_result in enumerate(self.results):
                for other_result in other_event.results:
                    if self_result == other_result:
                        break
                else:
                    deleted.append(self_index)
            if len(deleted) == len(self.results) - len(other_event.results):
                for r_index in reversed(deleted):
                    deleted_result = self.results.pop(r_index)
                    event_update_object.add_result_delete(r_index, deleted_result)
            else:
                raise ValueError("There is a mismatch between the expected number of deletes and how many deletes were attempted. This is indicative of a modification in the same action as a delete.")

        for index in range(max([len(self.results), len(other_event.results)])):
            if index < len(self.results):
                self_result = self.results[index]
            else:
                self_result = None
            if index < len(other_event.results):
                other_result = other_event.results[index]
            else:
                x=1
            if self_result and other_result:
                # See if I need to update an event
                update_result = self_result.update(other_result)
                if update_result:
                    event_update_object.add_result_update(index, update_result)
            elif self_result and not other_result:
                x=1
            elif not self_result and other_result:
                # Need to add a result
                event_update_object.add_result_create(other_result)
                # self.results.append(other_result)
                self.add_result(other_result)
            else:
                x=1

        if event_update_object:
            return event_update_object
        else:
            return None

    @classmethod
    def import_json(cls, json_data: str | dict):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        event_name = data.get('Event', None)
        event_time = data.get('Event Time', None)
        event_type = EventType.from_event_type_name(event_name)
        is_relay = data.get('relay', False)

        event_dict = {k: data.get(k) for k in ['Event', 'relay']}
        print('')
        print('')
        print(data['Event'])

        obj = cls(
            event_name=event_name,
            event_time=event_time,
            event_type=event_type,
            is_relay=is_relay,
        )
        team_key = 'Team 1'
        for team in data.get('teams', []):
            print('')
            print(f"TEAM: {team.get('name')}, {team.get('Heat/Lane/Flight')}")
            for athlete in team.get('athletes', []):
                if athlete['name'].startswith('Team'):
                    team_key = athlete['name']
                athlete = ResultDataObject.import_json(athlete, event_dict)
                obj.add_team_result(team_key, athlete)
            print(f"TEAM: {team}")
            # print(f"TEAM: {team.get('name')}, {team.get('Heat/Lane/Flight')}")
        for athlete in data.get('athletes', []):
            athlete = ResultDataObject.import_json(athlete, event_dict)
            obj.add_result(athlete)
        return obj

    def export_json(self):
        output = {
            'Event': self.event_name,
            'Event Time': self.event_time,
        }
        if self.is_relay:
            output['relay'] = self.is_relay

        """
        self.event_name = event_name
        self.event_time = event_time
        self.event_type = event_type
        self.is_relay = is_relay

        self.results = []
        self.team_team_results = {}

        """
        if self.results:
            output['athletes'] = []
        for result in self.results:
            result_json = result.export_json()
            output['athletes'].append(result_json)
        if self.team_team_results:
            output['teams'] = []
        for _, teams in self.team_team_results.items():
            for team_name, results in teams.items():
                tmp_team = {
                    'name': team_name,
                    'athletes': [],
                }
                for result in results:
                    result_json = result.export_json()
                    tmp_team['athletes'].append(result_json)
                output['teams'].append(tmp_team)
        return output

    def clean(self):
        if self.is_relay:
            if self.results:
                self.convert_to_relay()
            for school, teams in self.team_team_results.items():
                for team_name, results in teams.items():
                    for result_index in reversed(range(len(results))):
                        result = results[result_index]
                        if result.athlete.name == team_name:
                            self.team_team_results[school][team_name].pop(result_index)
        else:
            if self.team_team_results:
                self.convert_to_open()


class MeetDataObject(BespokeDataObjectBase):
    def __init__(self,
        meet_name: str,
        meet_date: date,
        small_meet: bool = False,
        jv_meet: bool = False,
        meet_location: str | None = None,
        last_updated: datetime | None = None,
        *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meet_name = meet_name
        self.meet_date = meet_date
        self.small_meet = small_meet
        self.jv_meet = jv_meet
        self.meet_location = meet_location
        self.last_updated = last_updated

        self.events = []

    def __iter__(self):
        return iter(self.events)

    def __repr__(self):
        return f"MeetDataObject(meet_name='{self.meet_name}', meet_date='{self.meet_date}', events_len={len(self.events)})"

    def __str__(self):
        return f"MeetDataObject(meet_name='{self.meet_name}', meet_date='{self.meet_date}', events_len={len(self.events)})"

    def add_event(self, event: EventDataObject, index: int | None = None):
        if index is not None:
            self.events.insert(index, event)
        else:
            self.events.append(event)

    def find_event(self, identifier: str | int) -> EventDataObject | None:
        if isinstance(identifier, str):
            for event in self.events:
                if event.event_name == identifier:
                    return event
            else:
                raise IndexError(f"EventDataObject with name {identifier} not found.")
        elif isinstance(identifier, int):
            try:
                return self.events[identifier]
            except IndexError:
                return None
        return None

    def remove_event(self, identifier: str | int):
        if isinstance(identifier, str):
            for event in self.events:
                if event.event_name == identifier:
                    self.events.remove(event)
                    return
            else:
                raise IndexError(f"EventDataObject with name {identifier} not found.")
        elif isinstance(identifier, int):
            self.events.pop(identifier)
            return

    def update(self, other_meet):
        meet_update_object = MeetUpdateObject()
        if self.meet_name != other_meet.meet_name:
            meet_update_object.add_update('meet_name', other_meet.meet_name)
            self.meet_name = other_meet.meet_name
        if self.meet_date != other_meet.meet_date:
            meet_update_object.add_update('meet_date', other_meet.meet_date)
            self.meet_date = other_meet.meet_date
        if self.small_meet != other_meet.small_meet:
            meet_update_object.add_update('small_meet', other_meet.small_meet)
            self.small_meet = other_meet.small_meet
        if self.jv_meet != other_meet.jv_meet:
            meet_update_object.add_update('jv_meet', other_meet.jv_meet)
            self.jv_meet = other_meet.jv_meet
        if self.meet_location != other_meet.meet_location:
            meet_update_object.add_update('meet_location', other_meet.meet_location)
            self.meet_location = other_meet.meet_location
        if self.last_updated != other_meet.last_updated:
            meet_update_object.add_update('last_updated', other_meet.last_updated)
            self.last_updated = other_meet.last_updated

        """
        If small meet changes, recalculate points?
        """

        # Deletion detection
        if len(self.events) > len(other_meet.events):
            deleted = []
            for self_index, self_event in enumerate(self.events):
                for other_event in other_meet.events:
                    if self_event == other_event:
                        break
                else:
                    deleted.append(self_index)
            if len(deleted) == len(self.events) - len(other_meet.events):
                for r_index in reversed(deleted):
                    deleted_result = self.events.pop(r_index)
                    meet_update_object.add_result_delete(r_index, deleted_result)
            else:
                raise ValueError("There is a mismatch between the expected number of deletes and how many deletes were attempted. This is indicative of a modification in the same action as a delete.")

        for index in range(max([len(self.events), len(other_meet.events)])):
            if index < len(self.events):
                self_event = self.events[index]
            else:
                self_event = None
            if index < len(other_meet.events):
                other_event = other_meet.events[index]
            else:
                x=1
            if self_event and other_event:
                update_result = self_event.update(other_event)
                if update_result:
                    meet_update_object.add_event_update(index, update_result)
            elif self_event and not other_event:
                x=1
            elif not self_event and other_event:
                meet_update_object.add_event_create(other_event)
                self.add_event(other_event)
            else:
                x=1

        if meet_update_object:
            return meet_update_object
        else:
            return None

    @property
    def events_name_list(self):
        return [event.event_name for event in self.events]

    @classmethod
    def import_json(cls, json_data: str | dict):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        meet = data.get('meet', {})
        events = data.get('events', [])
        meet_name = meet.get('meet_name', None)
        meet_date = meet.get('date', None)
        if meet_date:
            meet_date = datetime.strptime(meet_date, "%Y-%m-%d").date()
        small_meet = meet.get('small_meet', False)
        jv_meet = meet.get('jv_meet', False)
        last_updated = meet.get('last_updated', None)
        if last_updated:
            last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")
        obj = cls(
            meet_name=meet_name,
            meet_date=meet_date,
            small_meet=small_meet,
            jv_meet=jv_meet,
            # meet_location=meet_location,
            last_updated=last_updated,
        )
        for event in events:
            event_obj = EventDataObject.import_json(event)
            event_obj.clean()
            obj.add_event(event_obj)
        return obj

    def export_json(self):
        output = {
            'meet': {
                'meet_name': self.meet_name,
                'date': self.meet_date.strftime("%Y-%m-%d") if self.meet_date else None,
                'small_meet': self.small_meet,
                'jv_meet': self.jv_meet,
                'last_updated': self.last_updated.strftime("%Y-%m-%d %H:%M:%S") if self.last_updated else None,
            },
            'events': [],
        }
        for event in self.events:
            event_data = event.export_json()
            output['events'].append(event_data)
        return output

    @classmethod
    def from_file(cls, fl_obj):
        obj = cls.import_json(fl_obj.read())
        return obj

    def to_file(self, fl_obj):
        content = self.export_json()
        fl_obj.write(json.dumps(content, indent=4))


class ResultUpdateObject(BespokeUpdateObjectBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates = {}

    def add_update(self, key, value):
        self.updates[key] = value

    def add_result_update(self, index: int, result_update):
        if 'results' not in self.updates:
            self.updates['results'] = {}
        self.updates['results'][index] = result_update

    def __bool__(self):
        if self.updates:
            return True
        return False


class EventUpdateObject(BespokeUpdateObjectBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates = {}

    def add_update(self, key, value):
        self.updates[key] = value

    def add_result_update(self, index: int, result_update: ResultUpdateObject):
        if 'results' not in self.updates:
            self.updates['results'] = {}
        self.updates['results'][index] = result_update

    def add_result_create(self, result_data_object: ResultDataObject):
        if 'new_results' not in self.updates:
            self.updates['new_results'] = []
        self.updates['new_results'].append(result_data_object)

    def add_result_delete(self, index: int, result_data_object: ResultDataObject):
        if 'deleted_results' not in self.updates:
            self.updates['deleted_results'] = {}
        self.updates['deleted_results'][index] = result_data_object

    def __bool__(self):
        if self.updates:
            return True
        return False


class MeetUpdateObject(BespokeUpdateObjectBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.updates = {}

    def add_update(self, key, value):
        self.updates[key] = value

    def add_event_update(self, index: int, event_update: EventUpdateObject):
        if 'events' not in self.updates:
            self.updates['events'] = {}
        event_update.add_update_type(UpdateType.UPDATE)
        self.updates['events'][index] = event_update

    def add_event_create(self, event_data_object: EventDataObject):
        if 'new_events' not in self.updates:
            self.updates['new_events'] = []
        self.updates['new_events'].append(event_data_object)

    def add_result_delete(self, index: int, result_data_object: ResultDataObject):
        if 'deleted_results' not in self.updates:
            self.updates['deleted_results'] = {}
        self.updates['deleted_results'][index] = result_data_object

    def __bool__(self):
        if self.updates:
            return True
        return False


class UpdateResultObject:
    def __init__(self, update_object):
        self.update_object = update_object

    def thing(self):
        print(f"Meet updates:")
        for key, value in {k: v for k, v in self.update_object.updates.items() if k not in ['events', 'new_events', 'deleted_events']}.items():
            print(f"  {key}: {value}")
        for event_index, event_update_object in self.update_object.updates.get('events', {}).items():
            print(f"  Event Index: {event_index}")
            for key, value in {k: v for k, v in event_update_object.updates.items() if k not in ['results', 'new_results', 'deleted_results']}.items():
                print(f"    {key}: {value}")
            for result_index, result_update_object in event_update_object.updates.get('results', {}).items():
                print(f"    ResultData Index: {result_index}")
                for key, value in result_update_object.updates.items():
                    print(f"      {key}: {value}")
        for event_data_object in self.update_object.updates.get('new_events', []):
            print(f"  New Event: {event_data_object.event_name}")

    def walk(self):
        output  = []
        for key, value in {k: v for k, v in self.update_object.updates.items() if k != 'events'}.items():
            output.append(((key, value), None, None))
        for event_index, event_update_object in self.update_object.updates.get('events', {}).items():
            for key, value in {key: value for key, value in event_update_object.updates.items() if key != 'results'}.items():
                output.append((('event', event_index), (key, value), None))
            for result_index, result_update_object in event_update_object.updates.get('results', {}).items():
                for key, value in result_update_object.updates.items():
                    output.append((('event', event_index), ('result', result_index), (key, value)))
        return output

path = '/db/meets'
for fl in os.listdir(path):
    if fl.endswith('.json'):
        if 'Jack and Jill' in fl:
            continue
        if 'DELETEME' in fl:
            continue


        if 'copy'not in     fl:
            continue



        print(f"Loading {fl}...")
        with open(os.path.join(path, fl), 'r') as jf:
            meet = MeetDataObject.from_file(jf)
            # print(json.dumps(meet.export_json(), indent=4))
        new_fl = f"DELETEME_{fl}"
        meet.meet_name = meet.meet_name + ' -- TESTING'
        print(new_fl)
        with open(os.path.join(path, new_fl), 'w') as jf:
            meet.to_file(jf)
