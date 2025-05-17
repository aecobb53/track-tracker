# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError

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
        resp, content = call(
            'get',
            f"{TEST_URI}/meet/{meet_name}/{event_name}",
            assert_code=200,
        )
        print(f"FIND EVENT RESP: {dupe_resp}")
        print(f"FIND EVENT CONTENT: {dupe_content}")

        # Filter Events

        # # Update Event
        # print('Creating Event')
        # create_resp, create_content = call(
        #     'post',
        #     f"{TEST_URI}/meet/{meet_name}/{event_name}",
        # )
        # print(f"CREATE RESP: {create_resp}")
        # print(f"CREATE CONTENT: {create_content}")

        # # Reorder Event
        # print('Creating Event')
        # create_resp, create_content = call(
        #     'post',
        #     f"{TEST_URI}/meet/{meet_name}/{event_name}",
        # )
        # print(f"CREATE RESP: {create_resp}")
        # print(f"CREATE CONTENT: {create_content}")

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



    # # def test_pass(self):
    # #     assert True
    # #     meet_resp, meet_content = call(
    # #         'get',
    # #         f"{TEST_URI}/meet/{meet_name}/",
    # #         assert_code=200,
    # #     )
    # #     print(meet_resp)
    # #     print(meet_content)
    # #     # 1/0
    
    # def test_add_athletes(self):
    #     resp, content = call(
    #         'get',
    #         f"{TEST_URI}/meet/{meet_name}/",
    #     )
    #     print(resp)
    #     print(content)
    #     print('')
    #     print('')
    #     print(f"EVENT: {content['events']['Boys 100m']}")
    #     # content['events']['Boys 100m'].append()
    #     assert True
    #     1/0

    # def test_pass2(self):
    #     # assert True
    #     # meet_resp, meet_content = call(
    #     #     'post',
    #     #     f"{TEST_URI}/meet/{meet_name}2/",
    #     #     assert_code=200,
    #     # )
    #     # print(meet_resp)
    #     # print(meet_content)

    #     meet_resp, meet_content = call(
    #         'delete',
    #         f"{TEST_URI}/meet/{meet_name}2/",
    #         assert_code=200,
    #     )
    #     print(meet_resp)
    #     print(meet_content)
    #     1/0


    # def test_create_athlete(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/",
    #         assert_code=200,
    #     )
    #     validation_payload = {'athletes': []}
    #     self.assertEqual(
    #         content,
    #         validation_payload,
    #         f"Expected {validation_payload} but got {content}",
    #     )

    # def test_get_athletes(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/",
    #         assert_code=200,
    #     )
    #     validation_payload = {'athletes': []}
    #     self.assertEqual(
    #         content,
    #         validation_payload,
    #         f"Expected {validation_payload} but got {content}",
    #     )

    # def test_home(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/home",
    #         assert_code=200,
    #     )
    #     validation_payload = {'Hello': 'WORLD!'}
    #     self.assertEqual(
    #         content,
    #         validation_payload,
    #         f"Expected {validation_payload} but got {content}",
    #     )

    # def test_favicon(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/favicon.ico",
    #         assert_code=200,
    #     )

    # def test_robots(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/robots.txt",
    #         assert_code=200,
    #     )

    # # def test_about(self):
    # #     resp, content = call(
    # #         "get",
    # #         f"{TEST_URI}/",
    # #         assert_code=200,
    # #     )
    # #     validation_payload = {'Hello': 'WORLD!'}
    # #     self.assertEqual(
    # #         content,
    # #         validation_payload,
    # #         f"Expected {validation_payload} but got {content}",
    # #     )

    # # def test_service_info(self):
    # #     resp, content = call(
    # #         "get",
    # #         f"{TEST_URI}/",
    # #         assert_code=200,
    # #     )
    # #     validation_payload = {'Hello': 'WORLD!'}
    # #     self.assertEqual(
    # #         content,
    # #         validation_payload,
    # #         f"Expected {validation_payload} but got {content}",
    # #     )
