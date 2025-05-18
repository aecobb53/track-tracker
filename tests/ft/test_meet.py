# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError
import json
from .base_test_class import BaseTestClass, call, TEST_URI

# TEST_URI += "/meet"


class TestAthlete(BaseTestClass):
    def setUp(self):
        super().setUp()
        # Load Data
        self.create_meets()
        print(f"###DONE WITH SETUP###")
        print('')

    def tearDown(self):
        super().tearDown()
        # Clear Data
        pass

    def test_event_management(self):
        # Create Event
        print('Creating Event')
        meet_name = 'Testing Meet'
        event_name = 'Example Event'
        example_event = {
            'event_name': event_name,
            'event_time': None,
            'athletes': [],
        }
        create_resp, create_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            json=example_event,
            assert_code=201,
        )
        print(f"CREATE RESP: {create_resp}")
        print(f"CREATE CONTENT: {create_content}")

        print('Failing to Create a dupe Event')
        dupe_resp, dupe_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            json=example_event,
            assert_code=409,
        )
        print(f"CREATE DUPE RESP: {dupe_resp}")
        print(f"CREATE DUPE CONTENT: {dupe_content}")

        print('Verifying the Event shows up')
        resp, content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/",
            assert_code=200,
        )
        for event_item in content['events']:
            if event_item['event_name'] == event_name:
                break
        else:
            self.fail(f"Event {event_name} not found in events list")

        # Find Event
        print('Finding the Event')
        find_resp, find_content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=200,
        )
        print(f"FIND EVENT RESP: {find_resp}")
        print(f"FIND EVENT CONTENT: {find_content}")

        # Filter Events

        # Update Event
        print('Updating the Event Name')
        new_event_name = 'Updated Event'
        new_event = find_content.copy()
        new_event['event_name'] = new_event_name
        update_resp, update_content = call(
            'put',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            json=new_event,
            assert_code=200,
        )
        print(f"UPDATE EVENT RESP: {update_resp}")
        print(f"UPDATE EVENT CONTENT: {update_content}")
        print('Finding the updated Event')
        find_resp, find_content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{new_event_name}",
            assert_code=200,
        )
        print(f"FIND EVENT RESP: {find_resp}")
        print(f"FIND EVENT CONTENT: {find_content}")
        self.assertEqual(find_content['event_name'], new_event_name, f"Event name not updated to {new_event_name}")

        find_resp, find_content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=404,
        )
        print(f"FIND MISSING EVENT RESP: {find_resp}")
        print(f"FIND MISSING EVENT CONTENT: {find_content}")
        event_name = new_event_name

        # Reorder Event
        print('Reorder Event')
        reorder_resp, reorder_content = call(
            'put',
            f"{TEST_URI}/meet/{meet_name}/{event_name}/1",
            assert_code=200,
        )
        print(f"REORDER RESP: {reorder_resp}")
        print(f"REORDER CONTENT: {reorder_content}")
        print('Verifying the Event has been moved to the new index')
        resp, content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/",
            assert_code=200,
        )
        for event_item in content['events']:
            print(f"EVENT ITEM: {event_item}")
        self.assertEqual(content['events'][1]['event_name'], event_name, f"Event {event_name} not found in events list")

        # Delete Event
        print('Deleting Event')
        delete_resp, delete_content = call(
            'delete',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=200,
        )
        print(f"DELETING RESP: {delete_resp}")
        print(f"DELETING CONTENT: {delete_content}")

        delete_missing_resp, delete_missing_content = call(
            'delete',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=404,
        )
        print(f"DELETING MISSING RESP: {delete_missing_resp}")
        print(f"DELETING MISSING CONTENT: {delete_missing_content}")

        print('Verifying the Event does not show up')
        resp, content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/",
            assert_code=200,
        )
        for event_item in content['events']:
            if event_item['event_name'] == event_name:
                self.fail(f"Event {event_name} found in events list")
        find_resp, find_content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=404,
        )
        print(f"FIND MISSING EVENT RESP: {find_resp}")
        print(f"FIND MISSING EVENT CONTENT: {find_content}")

    def test_detailed_event(self):
        # Create Event
        print('Creating Event')
        meet_name = 'Testing Meet'
        event_name = 'Detailed Event'
        example_event = {
            'event_name': event_name,
            'event_time': '14:30',
            # 'athletes': [],
        }
        create_resp, create_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            json=example_event,
            assert_code=201,
        )
        print(f"CREATE RESP: {create_resp}")
        print(f"CREATE CONTENT: {create_content}")

        # Find Event
        print('Finding the Event')
        find_resp, find_content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=200,
        )
        print(f"FIND EVENT RESP: {find_resp}")
        print(f"FIND EVENT CONTENT: {find_content}")
        validate_event = {
            'event_name': event_name,
            'event_time': '14:30:00',
            'athletes': [],
            'is_relay': False,
            'meet_metadata': {},
            'gender': None,
        }
        self.assertEqual(find_content, validate_event, f"Event {event_name} not found in events list")

    def test_athlete_management(self):
        # Create Event
        print('Creating Event')
        meet_name = 'Testing Meet'
        event_name = 'Example Event'
        example_event = {
            'event_name': event_name,
            'event_time': None,
            'athletes': [],
        }
        create_resp, create_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            json=example_event,
            assert_code=201,
        )
        print(f"CREATE RESP: {create_resp}")
        print(f"CREATE CONTENT: {create_content}")
        print('Reorder Event')
        reorder_resp, reorder_content = call(
            'put',
            f"{TEST_URI}/meet/{meet_name}/{event_name}/0",
            assert_code=200,
        )
        print(f"REORDER RESP: {reorder_resp}")
        print(f"REORDER CONTENT: {reorder_content}")

        # Create Athletes
        print('Creating Athletes')
        athlete_1 = {
            'first_name': 'John',
            'last_name': 'Doe',
            'heat': 1,
            'lane': 3,
        }
        athlete_2 = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'heat': 1,
            'lane': 5,
        }
        athlete_3 = {
            'first_name': 'John',
            'last_name': 'Smith',
            'heat': 1,
            'lane': 4,
        }
        print('Creating Athlete 1')
        create_resp, create_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}/athlete",
            json=athlete_1,
            assert_code=201,
        )
        print(f"CREATE RESP: {create_resp}")
        print(f"CREATE CONTENT: {create_content}")

        print('Creating Athlete 3 (before athlete 2)')
        create_resp, create_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}/athlete",
            json=athlete_3,
            assert_code=201,
        )
        print(f"CREATE RESP: {create_resp}")
        print(f"CREATE CONTENT: {create_content}")

        print('Creating Athlete 2')
        create_resp, create_content = call(
            'post',
            f"{TEST_URI}/meet/{meet_name}/{event_name}/athlete",
            json=athlete_2,
            assert_code=201,
        )
        print(f"CREATE RESP: {create_resp}")
        print(f"CREATE CONTENT: {create_content}")

        # Find Event
        print('Finding the Event')
        find_resp, find_content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=200,
        )
        print(f"FIND EVENT RESP: {find_resp}")
        # print(f"FIND EVENT CONTENT: {find_content}")
        print(json.dumps(find_content, indent=4))   
        validation_event = {
            "event_name": event_name,
            "event_time": None,
            "gender": None,
            "athletes": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "team": None,
                    "graduation_year": None,
                    "flight": None,
                    "heat": 1,
                    "lane": 3,
                    "place": None,
                    "wind": None,
                    "result": None,
                    "meet_metadata": {}
                },
                {
                    "first_name": "John",
                    "last_name": "Smith",
                    "team": None,
                    "graduation_year": None,
                    "flight": None,
                    "heat": 1,
                    "lane": 4,
                    "place": None,
                    "wind": None,
                    "result": None,
                    "meet_metadata": {}
                },
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "team": None,
                    "graduation_year": None,
                    "flight": None,
                    "heat": 1,
                    "lane": 5,
                    "place": None,
                    "wind": None,
                    "result": None,
                    "meet_metadata": {}
                }
            ],
            "is_relay": False,
            "meet_metadata": {}
        }
        find_content_athletes = find_content.pop('athletes')
        validation_event_athletes = validation_event.pop('athletes')
        self.assertEqual(find_content, validation_event, f"Event {event_name} not found in events list")
        self.assertEqual(len(find_content_athletes), len(validation_event_athletes), f"Length of athletes do not match")
        for index, (a1, a2) in enumerate(zip(find_content_athletes, validation_event_athletes)):
            print(f"Comparing athlete {index}: {a1} vs {a2}")
            self.assertEqual(a1, a2, f"Athlete at index: [{index}] {a1} not the same as {a2}")
