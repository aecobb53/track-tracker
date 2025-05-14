from datetime import timedelta
from pydantic import BaseModel

from .event import EventParser


class Result(BaseModel):
    event_str: str
    result_str: str
    minutes: int | None = None
    seconds: int | None = None
    subsecond: float | None = None
    feet: int | None = None
    inches: int | None = None
    fractions: float | None = None

    @classmethod
    def parse_event_result(cls, event: str, result: str):
        if not result:
            result = ''
        minutes, seconds, subsecond, feet, inches, fractions = EventParser.parse_event_result(event_s=event, result_s=result)
        obj = cls(
            event_str=event,
            result_str=result,
            minutes=minutes,
            seconds=seconds,
            subsecond=subsecond,
            feet=feet,
            inches=inches,
            fractions=fractions,
        )
        return obj

    @property
    def format(self):
        minutes = str(self.minutes) if self.minutes is not None else None
        seconds = str(self.seconds) if self.seconds is not None else None
        subsecond = str(self.subsecond) if self.subsecond is not None else None

        feet = str(self.feet) if self.feet is not None else None
        inches = str(self.inches) if self.inches is not None else None
        fractions = str(self.fractions) if self.fractions is not None else None

        if all([minutes, seconds, subsecond]):
            return f"{minutes}:{seconds.zfill(2)}.{subsecond[2:]}"
        elif all([seconds, subsecond]):
            return f"{seconds}.{subsecond[2:]}"
        elif all([feet, inches, fractions]):
            return f"{feet}-{inches.zfill(2)}.{fractions[2:]}"
        elif all([feet, inches]):
            return f"{feet}-{inches}"

    @property
    def format_smaller_value(self):
        """
        Force results in terms of seconds or inches
        """
        """
        tmp = timedelta(
            minutes=minutes or 0,
            seconds=seconds or 0,
            milliseconds=subsecond or 0,
        )
        tmp_min = tmp.seconds // 60
        tmp_sec = tmp.seconds % 60
        tmp_microseconds = tmp.microseconds
        tmp_format = f"{tmp_min}:{tmp_sec}.{tmp_microseconds}"
        print(f"tmp: {tmp}, tmp_min: {tmp_min}, tmp_sec: {tmp_sec}, tmp_microseconds: {tmp_microseconds}, tmp_format: {tmp_format}")

        """
        if self.minutes or self.seconds or self.subsecond:
            minutes = self.minutes or 0
            seconds = self.seconds or 0
            subsecond = self.subsecond or 0
            seconds += subsecond
            value = timedelta(minutes=minutes, seconds=seconds)
            formatted = float(value.total_seconds())
            return formatted
        elif self.feet or self.inches or self.fractions:
            feet = self.feet or 0
            inches = self.inches or 0
            fractions = self.fractions or 0
            return feet * 12 + inches + fractions
        else:
            raise ValueError('Unable to give a Sort Value')

    @property
    def put(self):
        output = f"{self.event_str}::{self.result_str}"
        return output

    @property
    def sort_value(self):
        if self.minutes or self.seconds or self.subsecond:
            minutes = self.minutes or 0
            seconds = self.seconds or 0
            subsecond = self.subsecond or 0
            return minutes * 60 + seconds + subsecond
        elif self.feet or self.inches or self.fractions:
            feet = self.feet or 0
            inches = self.inches or 0
            fractions = self.fractions or 0
            return feet * 12 + inches + fractions
        else:
            raise ValueError('Unable to give a Sort Value')

    @property
    def is_none(self):
        return not any([
            self.minutes,
            self.seconds,
            self.subsecond,
            self.feet,
            self.inches,
            self.fractions,
        ])

    @classmethod
    def build(cls, input):
        event, result = input.split('::')
        return cls.parse_event_result(event=event, result=result)

    def __gt__(self, other):
        if self.seconds is not None and self.subsecond is not None and other.seconds is not None and other.subsecond is not None:
            # Its a time
            self_time = [
                self.minutes or 0,
                self.seconds or 0,
                self.subsecond or 0
            ]
            self_time = timedelta(minutes=self_time[0], seconds=self_time[1], milliseconds=self_time[2] * 1000)
            other_time = [
                other.minutes or 0,
                other.seconds or 0,
                other.subsecond or 0
            ]
            other_time = timedelta(minutes=other_time[0], seconds=other_time[1], milliseconds=other_time[2] * 1000)
            if other_time == timedelta(seconds=0) and self_time != timedelta(seconds=0):
                return True
            elif self_time < other_time:
                return True
            else:
                return False
        elif self.inches is not None and self.fractions is not None and other.inches is not None and other.fractions is not None:
            # Its a distance
            self_distance = [
                self.feet or 0,
                self.inches or 0,
                self.fractions or 0
            ]
            self_distance = self_distance[0] * 12 + self_distance[1] + self_distance[2]
            other_distance = [
                other.feet or 0,
                other.inches or 0,
                other.fractions or 0
            ]
            other_distance = other_distance[0] * 12 + other_distance[1] + other_distance[2]
            if self_distance > other_distance:
                return True
            else:
                return False
        elif self.is_none and not other.is_none:
            return True
        elif not self.is_none and other.is_none:
            return False
        else:
            print('Invalid Result dumping comparison')
            print(f"event_str: {self.event_str}, {other.event_str}")
            print(f"result_str: {self.result_str}, {other.result_str}")
            print(f"minutes: {self.minutes}, {other.minutes}")
            print(f"seconds: {self.seconds}, {other.seconds}")
            print(f"subsecond: {self.subsecond}, {other.subsecond}")
            print(f"feet: {self.feet}, {other.feet}")
            print(f"inches: {self.inches}, {other.inches}")
            print(f"fractions: {self.fractions}, {other.fractions}")
            raise ValueError('Invalid Result')

    def __eq__(self, other_object):
        if self.event_str != other_object.event_str:
            return False
        if self.result_str != other_object.result_str:
            return False
        if self.minutes != other_object.minutes:
            return False
        if self.seconds != other_object.seconds:
            return False
        if self.subsecond != other_object.subsecond:
            return False
        if self.feet != other_object.feet:
            return False
        if self.inches != other_object.inches:
            return False
        if self.fractions != other_object.fractions:
            return False
        return True
