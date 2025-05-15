from unittest import TestCase
import pytest
import requests

TEST_URI = "http://localhost:8205"


def call(
        method: str,
        path: str,
        body: dict = None,
        json: dict = None,
        params: dict = None,
        assert_code: int = None):
    call = {
        'url': path,
    }
    if body:
        call['json'] = body
    if json:
        call['json'] = json
    if params:
        call['params'] = params


    print(f"Making {method.upper()} request to {path}")
    for key, value in {k: v for k, v in call.items() if k != 'url'}.items():
        print(f"    {key}: {value}")
    resp = getattr(requests, method)(**call)
    print(f"    Response status code: {resp.status_code}")
    if not resp.ok:
        print(f"    Response content: {resp.content}")
        raise Exception(f"Request failed with status code {resp.status_code}")

    if assert_code is not None:
        print(f"    Expected status code: {assert_code}")
        assert resp.status_code == assert_code
    try:
        content = resp.json()
    except requests.JSONDecodeError:
        content = resp.content
    return resp, content


class BaseTestClass(TestCase):
    pass

    def create_athletes(self):
        print(f"POPULATING ATHLETE DATABASE")
        for athlete in generate_athletes():
            resp, content = call(
                "post",
                f"{TEST_URI}/athlete/",
                body=athlete,
                assert_code=201,
            )
            print(f"Response: {content}")
        print(f"DONE POPULATING ATHLETE DATABASE")

    def delete_all_athletes(self):
        print(f"CLEARING ATHLETE DATABASE")
        resp, content = call(
            "get",
            f"{TEST_URI}/athlete/"
        )
        for athlete in content['athletes']:
            resp, content = call(
                "delete",
                f"{TEST_URI}/athlete/{athlete['uid']}/",
            )
            print(f"Response: {content}")
        print(f"DONE CLEARING ATHLETE DATABASE")

    def create_results(self):
        print(f"POPULATING RESULTS DATABASE")
        for result in generate_results():
            resp, content = call(
                "post",
                f"{TEST_URI}/result/",
                body=result,
                assert_code=201,
            )
            print(f"Response: {content}")
        print(f"DONE POPULATING RESULTS DATABASE")

    def delete_all_results(self):
        print(f"CLEARING RESULTS DATABASE")
        resp, content = call(
            "get",
            f"{TEST_URI}/result/"
        )
        for result in content['results']:
            resp, content = call(
                "delete",
                f"{TEST_URI}/result/{result['uid']}/",
            )
            print(f"Response: {content}")
        print(f"DONE CLEARING RESULTS DATABASE")

    def setUp(self):
        # Load Data
        self.delete_all_results()
        self.delete_all_athletes()
        pass

    def tearDown(self):
        # Clear Data
        pass

def generate_athletes():
    athletes = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'graduation_year': 2025,
            'team': 'Fairview High School',
            'gender': 'Boys',
            # 'tags': List[str] = []
            # 'athlete_metadata': Dict[str, Any] = {}
        },
        {
            'first_name': 'Janie',
            'last_name': 'Doe',
            'first_nickname': 'Janie',
            'last_nickname': 'Doe',
            'graduation_year': 2025,
            'team': 'Fairview High School',
            'gender': 'Boys',
            # 'tags': List[str] = []
            # 'athlete_metadata': Dict[str, Any] = {}
        },
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'graduation_year': 2025,
            'team': 'Fairview High School',
        },
        # {
        #     'first_name': 'Jane',
        #     'last_name': 'Smith',
        #     'graduation_year': 2025,
        #     'team': 'Fairview High School',
        # },
    ]
    return athletes

def generate_results():
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
    return results
