# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError

from .base_test_class import BaseTestClass, call, TEST_URI

# TEST_URI += "/result"


class TestResult(BaseTestClass):
    def setUp(self):
        super().setUp()
        # Load Data
        # self.delete_all_results()
        # self.delete_all_athletes()
        self.create_athletes()
        self.create_results()
        print(f"###DONE WITH SETUP###")
        print('')

    def tearDown(self):
        super().tearDown()
        # Clear Data
        pass

    def test_from_milesplit(self):
        athlete = {
            'first_name': 'Example',
            'last_name': 'Example',
            'team': 'Fairview High School',
            'gender': 'Boys',
            'graduation_year': 2027
        }
        result = {
            'event': 'Boys 1600 Meter Run',
            'heat': 3,
            'place': 29,
            'wind': '',
            'team': 'Fairview High School',
            'points': 0,
            'meet_date': '2025-05-10',
            'result': '4:41.19',
            'meet': 'Meet',
            'gender': 'Boys',
            'result_metadata': {}
        }
        first = athlete['first_name']
        last = athlete['last_name']
        team = athlete['team']
        athlete_resp, athlete_content = call(
            'post',
            f"{TEST_URI}/athlete/",
            json=athlete,
            assert_code=201,
        )
        print(athlete_resp)
        result['athlete_uid'] = athlete_content['uid']
        result['athlete_first_name'] = athlete['first_name']
        result['athlete_last_name'] = athlete['last_name']

        result_resp, result_content = call(
            'post',
            f"{TEST_URI}/result/",
            json=result,
            assert_code=201,
        )
        print(result_resp)

        get_athlete_resp, get_athlete_content = call(
            'get',
            f"{TEST_URI}/athlete/{first}/{last}/{team}",
            params={'team': 'Fairview High School'},
            assert_code=200,
        )
        print(get_athlete_resp)
