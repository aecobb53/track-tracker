# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError

from .base_test_class import BaseTestClass, call, TEST_URI

TEST_URI += "/athlete"


class TestAthlete(BaseTestClass):
    def setUp(self):
        super().setUp()
        # Load Data
        # self.delete_all_results()
        # self.delete_all_athletes()
        self.create_athletes()
        pass

    def tearDown(self):
        super().tearDown()
        # Clear Data
        pass


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
