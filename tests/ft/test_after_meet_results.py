# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError
import json
from .base_test_class import BaseTestClass, call, TEST_URI

# TEST_URI += "/meet"


class TestAfterMeetResults(BaseTestClass):
    def setUp(self):
        super().setUp()
        # Load Data
        # self.create_meets()
        self.meet_1_name = "Testing Meet 1"
        self.meet_2_name = "Testing Meet 2"
        self.event_1_name = '100m Dash'
        self.event_2_name = '200m Dash'
        self.event_3_name = '400m Dash'
        self.event_4_name = '800m Dash'
        self.event_5_name = '4x100m Relay'
        self.create_meet_for_this_class()
        print(f"###DONE WITH SETUP###")
        print('')

    def tearDown(self):
        super().tearDown()
        # Clear Data
        pass

    def test_event_management(self):
        # Create Event
        print('Creating Event')
        assert True


    """
    Points for the year - or each year specified
    PR chart or graph - from year to year
    Verify you can reorder results based on place or result time since the test is simple right now
    """



    def create_meet_for_this_class(self):
        # MEET ONE
        meet_payload = {
            "meet_name": self.meet_1_name,
            'meet_date': "2025-01-01",
            'varsity_points': True,
            'small_meet': False,
            'auto_populate_events': False,
        }
        resp, content = call(
            'post',
            f"{TEST_URI}/meet/{self.meet_1_name}/",
            json=meet_payload,
            assert_code=201,
        )
        boy_names = ['James', 'Michael', 'John', 'Robert', 'David', 'William', 'Richard', 'Joseph', 'Thomas', 'Christopher']
        girl_names = ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Karen', 'Sarah']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        name_limiter = 20
        boy_names = boy_names
        girl_names = girl_names
        last_names = last_names[:int(name_limiter/2)]
        schools = ['Fairview', 'Cherry Creek', 'Columbine']
        # schools = ['Fairview']
        boy_athletes = []
        for i in range(name_limiter):
            if i > len(boy_names) - 1:
                first_name = boy_names[i % len(boy_names)]
            else:
                first_name = boy_names[i]

            if i > len(last_names) - 1:
                last_name = last_names[i % len(last_names)]
            else:
                last_name = last_names[i]
            if i > len(schools) - 1:
                school = schools[i % len(schools)]
            else:
                school = schools[i]

            boy_athletes.append({
                'first_name': first_name,
                'last_name': last_name,
                'team': school,
            })

        girl_athletes = []
        for i in range(name_limiter):
            if i > len(girl_names) - 1:
                first_name = girl_names[i % len(girl_names)]
            else:
                first_name = girl_names[i]
            if i > len(last_names) - 1:
                last_name = last_names[i % len(last_names)]
            else:
                last_name = last_names[i]
            if i > len(schools) - 1:
                school = schools[i % len(schools)]
            else:
                school = schools[i]

            girl_athletes.append({
                'first_name': first_name,
                'last_name': last_name,
                'team': school,
            })
        def create_event_and_add_athletes(event_name, girl_athletes, boy_athletes, athlete_offset):
            girls_event_name = f"Girls {event_name}"
            boys_event_name = f"Boys {event_name}"
            girl_athletes_adjusted = girl_athletes[athlete_offset:] + girl_athletes[:athlete_offset]
            boy_athletes_adjusted = boy_athletes[athlete_offset:] + boy_athletes[:athlete_offset]

            # GIRLS
            event_payload = {'event_name': girls_event_name}
            resp, content = call(
                'post',
                f"{TEST_URI}/meet/{self.meet_1_name}/{girls_event_name}",
                json=event_payload,
                assert_code=201,
            )
            for index, gaa in enumerate(girl_athletes_adjusted):
                lane_count = 8
                heat = int(index / lane_count) + 1
                lane = index % lane_count + 1
                athlete_payload = {
                    'first_name': gaa['first_name'],
                    'last_name': gaa['last_name'],
                    'team': gaa['team'],
                    'heat': heat,
                    'lane': lane,
                    'place': index + 1,
                }
                create_resp, create_content = call(
                    'post',
                    f"{TEST_URI}/meet/{self.meet_1_name}/{girls_event_name}/athlete",
                    json=athlete_payload,
                    assert_code=201,
                )


            # BOYS
            event_payload = {'event_name': boys_event_name}
            resp, content = call(
                'post',
                f"{TEST_URI}/meet/{self.meet_1_name}/{boys_event_name}",
                json=event_payload,
                assert_code=201,
            )
            for index, baa in enumerate(boy_athletes_adjusted):
                lane_count = 8
                heat = int(index / lane_count) + 1
                lane = index % lane_count + 1
                athlete_payload = {
                    'first_name': baa['first_name'],
                    'last_name': baa['last_name'],
                    'team': baa['team'],
                    'heat': heat,
                    'lane': lane,
                    'place': index + 1,
                }
                create_resp, create_content = call(
                    'post',
                    f"{TEST_URI}/meet/{self.meet_1_name}/{boys_event_name}/athlete",
                    json=athlete_payload,
                    assert_code=201,
                )

        create_event_and_add_athletes(self.event_1_name, girl_athletes, boy_athletes, 0)
        create_event_and_add_athletes(self.event_2_name, girl_athletes, boy_athletes, 2)
        create_event_and_add_athletes(self.event_3_name, girl_athletes, boy_athletes, 4)
        create_event_and_add_athletes(self.event_4_name, girl_athletes, boy_athletes, 6)

        """
        FIGURE OUT HOW TO ADD RELAY
        """

        for athlete in girl_athletes + boy_athletes:
            find_athlete_in_meet_resp, find_athlete_in_meet_content = call(
                'get',
                f"{TEST_URI}/meet/{self.meet_1_name}/athlete/{athlete['first_name']}/{athlete['last_name']}/{athlete['team']}",
                assert_code=200,
            )
            # print(f"FIND ATHLETE IN MEET RESP: {find_athlete_in_meet_resp}")
            # print(f"FIND ATHLETE IN MEET CONTENT: {find_athlete_in_meet_content}")
            # print(json.dumps(find_athlete_in_meet_content, indent=4))
            # raise Exception("STOP HERE")

        """
        Athlete get all results from a meet
        """

        """
        Athlete get all results from all meets
        """


        # raise Exception("STOP HERE")


        results = [
            {
                "event": "Boys 100m Dash",
                "heat": 1,
                "place": 1,
                "wind": 0.0,
                "athlete_first_name": "John",
                "athlete_last_name": "Doe",
                "team": "Fairview High School",
                "meet_date": "2025-01-01",
                "result": "11.23",
                "meet": "Test Meet",
                "points": 10,
            },
        ]

"""






"""
