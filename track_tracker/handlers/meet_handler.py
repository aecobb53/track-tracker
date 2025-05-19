import os
import json
from datetime import datetime
from sqlmodel import Session, select, func

# from .base_handler import BaseHandler
from .base_file_handler import BaseFileHandler
from models import (
    MeetEvent,
    Meet,
    MeetEventAthlete,
)
from html import display_date
from html.common import class_formatter

from .exceptions import MissingRecordException, DuplicateRecordsException, DataIntegrityException


class MeetHandler(BaseFileHandler):
    def __init__(self, meet_name: str, *args, **kwargs):
        self.file_name = f'meet_{meet_name}.json'
        super().__init__(file_name=self.file_name, file_directory='meet', *args, **kwargs)

        self.content = {}

    def save_file(self):
        self._saved_content = self.content.to_json  # Convert from pydantic to JSON
        super().save_file()

    def load_file(self):
        super().load_file()
        # self.content = self._saved_content  # Convert from JSON to pydantic
        self.content = Meet.from_json(self._saved_content)  # Convert from JSON to pydantic
        return self.content

    def move_file(self, new_directory: str):
        """
        Move the file to a new name
        """
        old_file_path = self.file_path
        self.file_directory = new_directory
        new_file_path = self.file_path
        self._ensure_directory()
        os.rename(old_file_path, new_file_path)

    def add_event(self, event: MeetEvent):
        """
        Add an event to the meet
        event_name: str
        event: dict - or eventually a pydantic object
        """
        self.load_file()
        for event_item in self.content.events:
            if event.event_name == event_item.event_name:
                raise DuplicateRecordsException(f"Event {event.event_name} already exists in meet {self.content.meet_name}")
        self.content.events.append(event)

    def find_event(self, event_name: str = None, event_index: int = None):
        self.load_file()
        if event_name:
            for index, event in enumerate(self.content.events):
                if event.event_name == event_name:
                    return event, index
            else:
                raise MissingRecordException(f"Event {event_name} does not exist in meet {self.content.meet_name}")
        elif event_index:
            if event_index < len(self.content.events):
                return event.events[event_index], event_index
            else:
                raise MissingRecordException(f"Event index {event_index} does not exist in meet {self.content.meet_name}")
        return None, None

    def update_event(self, event_name: str, event: MeetEvent):
        """
        Update an event in the meet
        event_name: str
        event: dict - or eventually a pydantic object
        """
        self.load_file()
        _, event_index = self.find_event(event_name=event_name)
        self.content.events[event_index] = event
        self.save_file()

    def move_event(self, new_event_index: int, event_name: str = None, event_index: int = None):
        """
        Update an event in the meet
        event_name: str
        event: dict - or eventually a pydantic object
        """
        self.load_file()
        _, event_index = self.find_event(event_name=event_name)
        event = self.content.events.pop(event_index)
        try:
            # Try to add the popped event to a new index
            self.content.events.insert(new_event_index, event)
            self.save_file()
        except Exception as e:
            # Try to add the popped event to the old index (or just dont save?)
            self.content.events.insert(event_index, event)
            raise DataIntegrityException(f"Event {event.event_name} cannot be moved to index {new_event_index} in meet {self.content.meet_name}") from e
        # self.save_file()

    def delete_event(self, event_name: str):
        """
        Delete an event from the meet
        event_name: str
        """
        self.load_file()
        for event_index in range(len(self.content.events)):
            if self.content.events[event_index].event_name == event_name:
                self.content.events.pop(event_index)
                break
        else:
            raise MissingRecordException(f"Event {event_name} does not exist in meet {self.content.meet_name}")

    def add_event_athlete(self, event_name: str, athlete: MeetEvent):
        """
        Add an athlete to an event in the meet
        event_name: str
        athlete: dict - or eventually a pydantic object
        """
        self.load_file()
        event, _ = self.find_event(event_name=event_name)
        event.athletes.append(athlete)
        self._assign_points_in_event(event=event)
        self._order_athletes_in_event(event=event)
        self.save_file()

    def find_event_athlete(self, event_name: str, first: str, last: str, team: str = None, suppress_exception: bool = False):
        event, _ = self.find_event(event_name=event_name)

        # Exact match
        for index, athlete in enumerate(event.athletes):
            if athlete.first_name == first and athlete.last_name == last:
                if team and athlete.team != team:
                    continue
                return athlete, index

        #  Case insensitive match
        for index, athlete in enumerate(event.athletes):
            if athlete.first_name.lower() == first.lower() and athlete.last_name.lower() == last.lower():
                if team and athlete.team.lower() != team.lower():
                    continue
                return athlete, index

        # Partial - case insensitive match
        for index, athlete in enumerate(event.athletes):
            if first.lower() in athlete.first_name.lower() and last.lower() in athlete.last_name.lower():
                if team and team.lower() not in athlete.team.lower():
                    continue
                return athlete, index

        # No match found
        if suppress_exception:
            return None, None
        else:
            raise MissingRecordException(f"Athlete {first} {last} does not exist in event {event_name} in meet {self.content.meet_name}")

    def find_athlete(self, first: str, last: str, team: str = None):
        events = []
        for event in self.content.events:
            result, index = self.find_event_athlete(event_name=event.event_name, first=first, last=last, team=team, suppress_exception=True)
            if result:
                events.append({
                    'event_name': event.event_name,
                    'athlete': result,
                    'index': index,
                })
        return events

    def update_event_athlete(self, event_name: str, first: str, last: str, athlete: MeetEventAthlete):
        """
        Update an athlete in an event in the meet
        event_name: str
        athlete: dict - or eventually a pydantic object
        """
        self.load_file()
        _, event_index = self.find_event(event_name=event_name)
        _, athlete_index = self.find_event_athlete(event_name=event_name, first=athlete.first_name, last=athlete.last_name)
        self.content.events[event_index].athletes[athlete_index] = athlete
        self._assign_points_in_event(event=self.content.events[event_index])
        self._order_athletes_in_event(event=self.content.events[event_index])
        self.save_file()

    def delete_event_athlete(self, event_name: str, first: str, last: str):
        """
        Delete an athlete from an event in the meet
        event_name: str
        athlete: dict - or eventually a pydantic object
        """
        self.load_file()
        _, event_index = self.find_event(event_name=event_name)
        _, athlete_index = self.find_event_athlete(event_name=event_name, first=first, last=last)
        self.content.events[event_index].athletes.pop(athlete_index)
        self.save_file()


    def _order_athletes_in_event(self, event: MeetEvent):
        """
        Order athletes in an event by their order
        """
        def sort_function(athlete: MeetEventAthlete):
            order = 0
            if athlete.flight:
                order = athlete.flight
            elif athlete.heat:
                order = athlete.heat
                if athlete.lane:
                    order = order + athlete.lane / 100
            return order
        event.athletes.sort(key=lambda x: sort_function(x))

    def _order_athletes_in_event_by_place(self, event: MeetEvent):
        """
        Order athletes in an event by their order
        """
        def sort_function(athlete: MeetEventAthlete, default: int):
            if athlete.place and isinstance(athlete.place, int):
                # A non int would be something like DNS / DNF / DQ
                return athlete.place
            else:
                return default
        missing_place = len(event.athletes) + 1
        event.athletes.sort(key=lambda x: sort_function(x, missing_place))

    def _assign_points_in_event(self, event: MeetEvent):
        """
        Assign points to athletes in an event
        """
        self._order_athletes_in_event_by_place(event=event)
        team_points_tracker = {}
        available_points = self.content.meet_point_values.copy()
        for athlete in event.athletes:
            if not available_points:
                break
            if athlete.team not in team_points_tracker:
                team_points_tracker[athlete.team] = []
            if len(team_points_tracker[athlete.team]) > self.content.max_school_scores:
                continue
            if not athlete.place or not isinstance(athlete.place, int):
                # Its a non valid point scoring place
                continue
            athlete.points = available_points.pop(0)
            team_points_tracker[athlete.team].append(athlete)
