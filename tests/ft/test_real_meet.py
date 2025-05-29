# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError
import json
from .base_test_class import BaseTestClass, call, TEST_URI

# TEST_URI += "/meet"



"""
Location
Meet Date

Set up a patch update endpoint from the front end?
Set up a get patch style endpoint for the front end?

Set up tests for jumps and throws just to focus on minute details
"""




class TestRealMeet(BaseTestClass):
    def setUp(self):
        super().setUp()
        # Load Data
        # self.create_meets()
        print(f"###DONE WITH SETUP###")
        print('')

    def tearDown(self):
        super().tearDown()
        # Clear Data
        pass

    def test_real_meet(self):
        # self.skipTest("This test is not run in CI")


        upload_path = '/home/acobb/git/track-tracker/etc/tmp/upload_file.json'
        with open(upload_path, 'r') as f:
            data = json.load(f)
        for year, year_meets in data.items():
            print(f"YEAR: {year}")
            for meet_name, meet_events in year_meets.items():
                print(f"MEET NAME: {meet_name}")
                meet_payload = {
                    "meet_name": meet_name,
                    'auto_populate_events': False,
                }
                create_meet_resp, create_meet_content = call(
                    'post',
                    f"{TEST_URI}/meet/{meet_name}/",
                    json=meet_payload,
                    assert_code=201,
                )
                # print(f"RESP: {create_meet_resp}")
                if create_meet_resp.status_code != 201:
                    # print(f"MEET CONTENT: {create_meet_content}")
                    self.assertEqual(create_meet_resp.status_code, 201)

                for event_name, event_results in meet_events.items():
                    print(f"EVENT NAME: {event_name}")
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
                    # print(f"CREATE RESP: {create_resp}")
                    if create_resp.status_code != 201 and create_resp.status_code != 409:
                        print(f"CREATE RESP: {create_resp}")
                        print(f"CREATE CONTENT: {create_content}")
                        self.assertEqual(True, False, f"This is just to trigger an error")

                    for result in event_results:
                        # print(f"RESULT: {result}")
                        athlete = result['athlete']
                        result = result['result']
                        athlete_payload = {
                            'first_name': athlete['first_name'],
                            'last_name': athlete['last_name'],
                            'team': athlete['team'],
                            'graduation_year': athlete['graduation_year'],
                            'flight': result.get('flight'),
                            'heat': result.get('heat'),
                            'lane': result.get('lane'),
                            'place': result.get('place'),
                            'wind': result.get('wind') if result.get('wind') else None,
                            'result': result.get('result'),
                            'event_name': event_name,
                        }
                        # print(f"ATHLETE PAYLOAD: {athlete_payload}")
                        create_resp, create_content = call(
                            'post',
                            f"{TEST_URI}/meet/{meet_name}/{event_name}/athlete",
                            json=athlete_payload,
                            assert_code=201,
                        )
                        # print(f"CREATE RESP: {create_resp}")
                        # print(f"CREATE CONTENT: {create_content}")
                        # if not create_resp.ok:
                        #     print(f"CREATE PAYLOAD: {athlete_payload}")
                        #     print(f"CREATE RESP: {create_resp}")
                        #     print(f"CREATE CONTENT: {create_content}")
                        #     self.assertEqual(create_resp.status_code, 201)
                # print('VERIFY EVENT:')
                # verify_resp, verify_content = call(
                #     'get',
                #     f"{TEST_URI}/meet/{meet_name}/{event_name}",
                #     assert_code=200,
                # )
                # print(f"VERIFY EVENT RESP: {verify_resp}")
                # print(f"VERIFY EVENT CONTENT: {verify_content}")
            # print('VERIFY MEET:')
            # verify_resp, verify_content = call(
            #     'get',
            #     f"{TEST_URI}/meet/{meet_name}",
            #     assert_code=200,
            # )
            # print(f"VERIFY MEET RESP: {verify_resp}")
            # print(f"VERIFY MEET CONTENT: {verify_content}")
        # assert False
