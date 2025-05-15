
import json
import os

from datetime import datetime, date, time, timedelta
from enum import Enum


x=1

"""
WARNING: Things get messed up if you try to modify in the same update as a delete.
It is best to do modifications, adds, and deletes in separate updates.
"""



"""
class Result:
    def __init__(self, result: str):
        self.result = result

    def __eq__(self, other_object: object) -> bool:
        if getattr(self, 'result', None) != getattr(other_object, 'result', None):
            return False
        return True


class MSAthlete:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other_object: object) -> bool:
        if getattr(self, 'name', None) != getattr(other_object, 'name', None):
            return False
        return True
"""



class Result:
    """
    This is a mock for right now
    """
    def __init__(self, result: str):
        self.result = result

    def __eq__(self, other_object: object) -> bool:
        if other_object is None:
            # This occurs more often than I expected
            return False
        if self.result != other_object.result:
            return False
        return True


class MSAthlete:
    """
    This is a mock for right now
    """
    def __init__(self, name: str, team: str):
        self.name = name
        self.team = team

    def __eq__(self, other_object: object) -> bool:
        if self.name != other_object.name:
            return False
        if self.team != other_object.team:
            return False
        return True


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


class MSResultDataObject(BespokeDataObjectBase):
    def __init__(self,
        athlete: MSAthlete,
        seed: Result | None = None,
        result: Result | None = None,
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
        return f"MSResultDataObject(athlete='{self.athlete.name}', result='{self.result.result if self.result else None}', place={self.place})"

    def __str__(self):
        return f"MSResultDataObject(athlete='{self.athlete.name}', result='{self.result.result if self.result else None}', place={self.place})"

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
    def import_json(cls, json_data: str | dict):
        if isinstance(json_data, str):
            data = json.loads(json_data)
        elif isinstance(json_data, dict):
            data = json_data
        x=1
        """
        THIS WILL NEED TO BE UPDAT4ED BEFORE ADDING TO SERVICE
        """
        athlete = MSAthlete(
            data.get('name', 'Unknown'),
            data.get('team', 'School'),
        )
        seed = Result(data.get('seed', None))
        result = Result(data.get('seed', None))
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

    def find_result(self, identifier: str | int) -> MSResultDataObject | None:
        if isinstance(identifier, str):
            for result in self.results:
                if result.athlete.name == identifier:
                    return result
            else:
                raise IndexError(f"MSResultDataObject with name {identifier} not found.")
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
                raise IndexError(f"MSResultDataObject with name {identifier} not found.")
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
                team_name = f"Team {team_pointer_int}"
                if team_name not in teams[result.athlete.team]:
                    teams[result.athlete.team][team_name] = []
                if len(teams[result.athlete.team][team_name]) < 4:
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
            x=1
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

        obj = cls(
            event_name=event_name,
            event_time=event_time,
            event_type=event_type,
            is_relay=is_relay,
        )
        if not is_relay:
            for athlete in data.get('athletes', []):
                obj.add_result(MSResultDataObject.import_json(athlete))
        return obj


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
            x=1
            if index < len(self.events):
                self_event = self.events[index]
            else:
                self_event = None
            if index < len(other_meet.events):
                other_event = other_meet.events[index]
            else:
                x=1
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
            obj.add_event(event_obj)
        x=1
        return obj

    @classmethod
    def from_file(cls, fl_obj):
        obj = cls.import_json(fl_obj.read())
        return obj


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

    def add_result_create(self, result_data_object: MSResultDataObject):
        if 'new_results' not in self.updates:
            self.updates['new_results'] = []
        self.updates['new_results'].append(result_data_object)

    def add_result_delete(self, index: int, result_data_object: MSResultDataObject):
        if 'deleted_results' not in self.updates:
            self.updates['deleted_results'] = {}
        self.updates['deleted_results'][index] = result_data_object

    def __bool__(self):
        if self.updates:
            return True
        return False


class MeetUpdateObject(BespokeUpdateObjectBase):
    def __init__(self, *args, **kwargs):
        # super().__init__(update_types=[UpdateType.UPDATE], *args, **kwargs)
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

    def add_result_delete(self, index: int, result_data_object: MSResultDataObject):
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
        # self.event_pointer = 0
        # self.result_pointer = 0

    def thing(self):
        x=1
        print(f"Meet updates:")
        for key, value in {k: v for k, v in self.update_object.updates.items() if k not in ['events', 'new_events', 'deleted_events']}.items():
            print(f"  {key}: {value}")
        for event_index, event_update_object in self.update_object.updates.get('events', {}).items():
            print(f"  Event Index: {event_index}")
            for key, value in {k: v for k, v in event_update_object.updates.items() if k not in ['results', 'new_results', 'deleted_results']}.items():
                print(f"    {key}: {value}")
            for result_index, result_update_object in event_update_object.updates.get('results', {}).items():
                print(f"    Result Index: {result_index}")
                for key, value in result_update_object.updates.items():
                    print(f"      {key}: {value}")
                x=1
        for event_data_object in self.update_object.updates.get('new_events', []):
            print(f"  New Event: {event_data_object.event_name}")

        x=1

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

def gen_base_meet():
    meet = MeetDataObject("Test MeetDataObject", date(2025,1,1), False, False, "Test Location")

    e1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
    e2 = EventDataObject("200m", time(12, 30), EventType(True, False, True, False, False, False, False))
    e3 = EventDataObject("Shot Put", time(13, 0), EventType(False, True, False, False, True, False, False))
    x=1

    a1 = MSAthlete("John Doe", 'School')
    a2 = MSAthlete("Jane Smith", 'School')
    a3 = MSAthlete("Bob Johnson", 'School')


    e1.add_result(MSResultDataObject(a1, result=Result(12.5), place=1))
    e1.add_result(MSResultDataObject(a2, result=Result(12.5), place=1))
    e1.add_result(MSResultDataObject(a3, result=Result(12.6), place=3))

    e2.add_result(MSResultDataObject(a1))
    e2.add_result(MSResultDataObject(a2))
    e2.add_result(MSResultDataObject(a3))


    meet.add_event(e1)
    meet.add_event(e2)
    meet.add_event(e3, 1)
    return meet

def gen_real_meet():
    path = '/home/acobb/git/track-tracker/persisted_db/meets/BOCO Championships.json'
    with open(path, 'r') as jf:
        meet = MeetDataObject.import_json(jf.read())
    return meet


# x=1
# m = MeetDataObject("Test MeetDataObject", datetime.now(), False, False, "Test Location")
# e1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
# e2 = EventDataObject("200m", time(12, 30), EventType(True, False, True, False, False, False, False))
# e3 = EventDataObject("Shot Put", time(13, 0), EventType(False, True, False, False, True, False, False))
# x=1
# m.add_event(e1)
# m.add_event(e2)
# m.add_event(e3, 1)

# for i in m.events_name_list:
#     print(i)

# print('---')

# m.remove_event(1)
# m.remove_event("100m")
# # m.remove_event("100m")
# # m.remove_event(5)

# for i in m.events_name_list:
#     print(i)

# x=1
# meet = MeetDataObject("Test MeetDataObject", date(2025,1,1), False, False, "Test Location")

# e1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
# e2 = EventDataObject("200m", time(12, 30), EventType(True, False, True, False, False, False, False))
# e3 = EventDataObject("Shot Put", time(13, 0), EventType(False, True, False, False, True, False, False))
# x=1

# a1 = MSAthlete("John Doe")
# a2 = MSAthlete("Jane Smith")
# a3 = MSAthlete("Bob Johnson")


# e1.add_result(MSResultDataObject(a1, result=Result(12.5), place=1))
# e1.add_result(MSResultDataObject(a2, result=Result(12.5), place=1))
# e1.add_result(MSResultDataObject(a3, result=Result(12.6), place=3))

# e2.add_result(MSResultDataObject(a1))
# e2.add_result(MSResultDataObject(a2))
# e2.add_result(MSResultDataObject(a3))


# meet.add_event(e1)
# meet.add_event(e2)
# meet.add_event(e3, 1)

# print(f"MEET: {meet}")
# for event in meet:
#     print(f"  Event: {event}")
#     x=1
#     for result in event.results:
#         print(f"    Result: {result}")
#         x=1

x=1


# path = '/home/acobb/git/track-tracker/persisted_db/meets/BOCO Championships.json'
# with open(path, 'r') as jf:
#     meet = MeetDataObject.import_json(jf.read())

# print(f"MEET: {meet}")
# for event in meet:
#     print(f"  Event: {event}")
#     x=1
#     for result in event.results:
#         print(f"    Result: {result}")
#         x=1

x=1

meet = gen_base_meet()

print(f"MEET: {meet}")
for event in meet:
    print(f"  Event: {event}")
    x=1
    for result in event.results:
        print(f"    Result: {result}")
        x=1
print('-----')

meet2 = gen_base_meet()
# meet2.meet_name = "Updated meet object"
# meet2.events[0].results[0].seed = Result(12.5)
# meet2.events[0].results[0].athlete = MSAthlete("Jain Doe")
# meet2.events[1].event_time = "13:15"
# meet2.jv_meet = True

# e4 = EventDataObject("400m", time(13, 0), EventType(False, True, False, False, True, False, False))
# meet2.events[0].add_result(MSResultDataObject(MSAthlete("New MSAthlete"), result=Result(12.5), place=1))
# meet2.add_event(e4)
meet2.events.pop(1)
# meet2.events[0].results.pop(1)
# meet2.events[0].results.pop(-1)
x=1

print(f"MEET2: {meet2}")
for event in meet2:
    print(f"  Event: {event}")
    x=1
    for result in event.results:
        print(f"    Result: {result}")
        x=1
print('-----')

update_result = meet.update(meet2)
update_obj = UpdateResultObject(update_result)
update_obj.thing()

x=1
print('--------')
for thing in update_obj.walk():
    print(f"THING: {thing}")
    x=1
x=1
print('--------')


print(f"MEET UPDATED: {meet}")
for event in meet:
    print(f"  Event: {event}")
    x=1
    for result in event.results:
        print(f"    Result: {result}")
        x=1
# print('-----')

# meet3 = gen_real_meet()
# print('-----')
# print(f"MEET3: {meet3}")
# for event in meet3:
#     print(f"  Event: {event}")
#     x=1
#     for result in event.results:
#         print(f"    Result: {result}")
#         x=1

x=1


"""
TEST BLOCK
"""

def generate_base_meet():
    meet = MeetDataObject("Test MeetDataObject", date(2025,1,1), False, False, "Test Location")

    event_1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
    event_2 = EventDataObject("200m", time(12, 30), EventType(True, False, True, False, False, False, False))
    event_3 = EventDataObject("Shot Put", time(13, 0), EventType(False, True, False, False, True, False, False))
    event_4 = EventDataObject("400m", time(13, 0), EventType(False, True, False, False, True, False, False))
    event_5 = EventDataObject("Long Jump", time(13, 0), EventType(False, True, False, False, True, False, False))

    athlete_1 = MSAthlete("John Doe", "School")
    athlete_2 = MSAthlete("Jane Smith", "School")
    athlete_3 = MSAthlete("Bob Johnson", "School")
    athlete_4 = MSAthlete("Alice Brown", "School")
    athlete_5 = MSAthlete("Charlie Davis", "School")

    # Event 1 has results and places
    event_1.add_result(MSResultDataObject(athlete_1, result=Result(12.5), place=1))
    event_1.add_result(MSResultDataObject(athlete_2, result=Result(12.5), place=1))
    event_1.add_result(MSResultDataObject(athlete_3, result=Result(12.6), place=3))

    # Event 2 has athletes but no results
    event_2.add_result(MSResultDataObject(athlete_1))
    event_2.add_result(MSResultDataObject(athlete_2))
    event_2.add_result(MSResultDataObject(athlete_3))

    # Event 3 has nothing

    # Event 4 has results
    event_4.add_result(MSResultDataObject(athlete_3, result=Result(50.0), place=1))
    event_4.add_result(MSResultDataObject(athlete_4, result=Result(50.5), place=2))
    event_4.add_result(MSResultDataObject(athlete_5, result=Result(51.0), place=3))

    # Event 5 has results
    event_5.add_result(MSResultDataObject(athlete_1, result=Result(5.0), place=1))
    event_5.add_result(MSResultDataObject(athlete_3, result=Result(4.8), place=2))
    event_5.add_result(MSResultDataObject(athlete_5, result=Result(4.9), place=3))

    meet.add_event(event_1)
    meet.add_event(event_2)
    meet.add_event(event_3)
    meet.add_event(event_4)
    meet.add_event(event_5)
    return meet

def load_meet_from_file(file_path):
    """
    Load a meet from a JSON file.
    """
    with open(file_path, 'r') as jf:
        meet = MeetDataObject.import_json(jf.read())
    return meet

def test_simple_create():
    """
    Creating a meet with some diversity but injecting an event between other events.
    """
    meet = MeetDataObject("Test MeetDataObject", date(2025,1,1), False, False, "Test Location")

    event_1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
    event_2 = EventDataObject("200m", time(12, 30), EventType(True, False, True, False, False, False, False))
    event3 = EventDataObject("Shot Put", time(13, 0), EventType(False, True, False, False, True, False, False))

    athlete_1 = MSAthlete("John Doe", "School")
    athlete_2 = MSAthlete("Jane Smith", "School")
    athlete_3 = MSAthlete("Bob Johnson", "School")

    event_1.add_result(MSResultDataObject(athlete_1, result=Result(12.5), place=1))
    event_1.add_result(MSResultDataObject(athlete_2, result=Result(12.5), place=1))
    event_1.add_result(MSResultDataObject(athlete_3, result=Result(12.6), place=3))

    event_2.add_result(MSResultDataObject(athlete_1))
    event_2.add_result(MSResultDataObject(athlete_2))
    event_2.add_result(MSResultDataObject(athlete_3))

    meet.add_event(event_1)
    meet.add_event(event_2)
    meet.add_event(event3, 1)
    assert meet.events[0].event_name == "100m"
    assert meet.events[1].event_name == "Shot Put"
    assert meet.events[2].event_name == "200m"

def test_modify_meet():
    """
    Test modifying a meet by changing values here and there.
    """
    meet1 = generate_base_meet()
    meet2 = generate_base_meet()

    meet2.events[0].results[0].athlete = MSAthlete("New MSAthlete", "School")
    meet2.events[0].results[0].seed = Result(12.5)

    meet2.events[0].event_time = time(13, 15)

    meet2.meet_name = "Updated meet object"

    meet2.events[2].event_name = "Updated Event Name"

    meet2.events[4].event_name = "Updated Event Name 2"
    meet2.events[4].results[1].seed = Result(10.0)
    meet2.events[4].results[2].athlete = MSAthlete("Updated MSAthlete", "School")


    update_object = meet1.update(meet2)
    assert update_object.updates['meet_name'] == "Updated meet object"
    assert update_object.updates['events'][0].updates['event_time'] == time(13, 15)
    assert update_object.updates['events'][0].updates['results'][0].updates['athlete'].name == 'New MSAthlete'
    assert update_object.updates['events'][0].updates['results'][0].updates['seed'].result == 12.5

    assert update_object.updates['events'][2].updates['event_name'] == "Updated Event Name"
    assert update_object.updates['events'][4].updates['event_name'] == "Updated Event Name 2"
    assert update_object.updates['events'][4].updates['results'][1].updates['seed'].result == 10.0
    assert update_object.updates['events'][4].updates['results'][2].updates['athlete'].name == "Updated MSAthlete"

def test_add_to_meet():
    """
    Test adding events and results.
    """
    meet1 = generate_base_meet()
    meet2 = generate_base_meet()

    meet2.events[0].add_result(MSResultDataObject(MSAthlete("New MSAthlete", "School"), result=Result(12.5), place=1))

    meet2.add_event(EventDataObject("New Event", time(14, 0), EventType(True, False, True, False, False, False, False)))

    update_object = meet1.update(meet2)
    assert isinstance(update_object.updates['new_events'][0], EventDataObject)
    assert isinstance(update_object.updates['events'][0].updates['new_results'][0], MSResultDataObject)

def test_delete_from_meet():
    """
    Test deleting events and results.
    """
    meet1 = generate_base_meet()
    meet2 = generate_base_meet()

    del meet2.events[0].results[0]
    del meet2.events[3].results[1]
    del meet2.events[4].results[2]

    update_object_1 = meet1.update(meet2)

    assert update_object_1.updates['events'][0].updates['deleted_results'][0].athlete.name == "John Doe"
    assert update_object_1.updates['events'][3].updates['deleted_results'][1].athlete.name == "Alice Brown"
    assert update_object_1.updates['events'][4].updates['deleted_results'][2].athlete.name == "Charlie Davis"

    meet3 = generate_base_meet()
    meet4 = generate_base_meet()

    del meet4.events[4]
    del meet4.events[2]
    del meet4.events[0]

    update_object_2 = meet3.update(meet4)

    assert update_object_2.updates['deleted_results'][4].event_name == "Long Jump"
    assert update_object_2.updates['deleted_results'][2].event_name == "Shot Put"
    assert update_object_2.updates['deleted_results'][0].event_name == "100m"

def test_different_add_update_delete_functions():
    result_1 = MSResultDataObject(MSAthlete("John Doe", "School"), result=Result(12.5), place=1)
    result_2 = MSResultDataObject(MSAthlete("Jane Smith", "School"), result=Result(12.5), place=1)
    result_3 = MSResultDataObject(MSAthlete("Bob Johnson", "School"), result=Result(12.6), place=3)

    event_1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
    event_2 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))
    assert event_1 == event_2

    event_1.add_result(result_1)
    event_1.add_result(result_2)
    event_1.add_result(result_3)
    event_2.add_result(result_1)
    event_2.add_result(result_2)
    event_2.add_result(result_3)

    assert event_1 == event_2
    event_1.remove_result(result_2.athlete.name)
    assert event_1 != event_2
    event_1.add_result(result_2, 1)
    assert event_1 == event_2

    result = event_1.find_result(result_2.athlete.name)
    assert result == result_2

    for thing in event_1:
        pass

def test_event_relay_handling():
    result_1 = MSResultDataObject(MSAthlete("John Doe", "School"), result=Result(12.5), place=1)
    result_2 = MSResultDataObject(MSAthlete("Jane Smith", "School"), result=Result(12.5), place=1)
    result_3 = MSResultDataObject(MSAthlete("Bob Johnson", "School"), result=Result(12.6), place=3)
    result_4 = MSResultDataObject(MSAthlete("Jack Doe", "School"), result=Result(12.5), place=1)

    result_5 = MSResultDataObject(MSAthlete("John Doe 2", "School 2"), result=Result(12.5), place=1)
    result_6 = MSResultDataObject(MSAthlete("Jane Smith 2", "School 2"), result=Result(12.5), place=1)
    result_7 = MSResultDataObject(MSAthlete("Bob Johnson 2", "School 2"), result=Result(12.6), place=3)
    result_8 = MSResultDataObject(MSAthlete("Jack Doe 2", "School 2"), result=Result(12.5), place=1)
    # result_9 = MSResultDataObject(MSAthlete("Blake Doe 2", "School 2"), result=Result(12.5), place=1)

    result_11 = MSResultDataObject(MSAthlete("John Doe 3", "School"), result=Result(12.5), place=1)
    result_12 = MSResultDataObject(MSAthlete("Jane Smith 3", "School"), result=Result(12.5), place=1)
    result_13 = MSResultDataObject(MSAthlete("Bob Johnson 3", "School"), result=Result(12.6), place=3)
    result_14 = MSResultDataObject(MSAthlete("Jack Doe 3", "School"), result=Result(12.5), place=1)

    result_21 = MSResultDataObject(MSAthlete("John Doe 4", "School 3"), result=Result(12.5), place=1)
    result_22 = MSResultDataObject(MSAthlete("Jane Smith 4", "School 3"), result=Result(12.5), place=1)
    result_23 = MSResultDataObject(MSAthlete("Bob Johnson 4", "School 3"), result=Result(12.6), place=3)
    result_24 = MSResultDataObject(MSAthlete("Jack Doe 4", "School 3"), result=Result(12.5), place=1)
    result_25 = MSResultDataObject(MSAthlete("Jack Doe 4", "School 3"), result=Result(12.5), place=1)

    event_1 = EventDataObject("100m", time(12, 0), EventType(True, False, True, False, False, False, False))

    event_1.add_result(result_1)
    event_1.add_result(result_2)
    event_1.add_result(result_3)
    event_1.add_result(result_4)

    event_1.add_result(result_5)
    event_1.add_result(result_6)
    event_1.add_result(result_7)
    event_1.add_result(result_8)

    event_1.add_result(result_11)
    event_1.add_result(result_12)
    event_1.add_result(result_13)
    event_1.add_result(result_14)

    event_1.add_team_result('Team 1', result_1)
    event_1.add_team_result('Team 1', result_2)
    event_1.add_team_result('Team 1', result_3)
    # event_1.add_team_result('Team 1', result_4)

    event_1.add_team_result('Team 1', result_21)
    event_1.add_team_result('Team 1', result_22)
    event_1.add_team_result('Team 1', result_23)
    event_1.add_team_result('Team 1', result_24)
    event_1.add_team_result('Team 1', result_25)

    event_1.convert_to_relay()
    assert event_1.is_relay == True
    assert event_1.results == []
    assert 'School 2' in event_1.team_team_results
    assert 'School' in event_1.team_team_results
    assert 'Team 1' in event_1.team_team_results['School']
    assert 'Team 2' in event_1.team_team_results['School']

    assert event_1.team_team_results['School']['Team 1'] == [result_1, result_2, result_3, result_4]
    assert event_1.team_team_results['School']['Team 2'] == [result_11, result_12, result_13, result_14]
    assert event_1.team_team_results['School 2']['Team 1'] == [result_5, result_6, result_7, result_8]
    assert event_1.team_team_results['School 3']['Team 1'] == [result_21, result_22, result_23, result_24, result_25]

    event_1.add_result(result_1)
    event_1.add_result(result_2)
    event_1.add_result(result_3)
    event_1.add_result(result_4)

    event_1.convert_to_open()

    assert event_1.is_relay == False
    assert event_1.team_team_results == {}
    assert len(event_1.results) == 16

def test_real_world():
    path = '/home/acobb/git/track-tracker/persisted_db/meets'
    meets = []
    for fl in os.listdir(path):
        if fl.endswith('.json'):
            with open(os.path.join(path, fl), 'r') as f:
                meet = MeetDataObject.from_file(f)
                meets.append(meet)
                x=1
    x=1


test_simple_create()
test_modify_meet()
test_add_to_meet()
test_delete_from_meet()
test_different_add_update_delete_functions()
test_event_relay_handling()

test_real_world()

x=1

# Workout