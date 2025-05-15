# from unittest import TestCase
# import pytest
# import requests
# from requests import JSONDecodeError

from .base_test_class import BaseTestClass, call, TEST_URI


class TestServerBaseAPI(BaseTestClass):
    def test_empty_path(self):
        resp, content = call(
            "get",
            f"{TEST_URI}/",
            assert_code=200,
        )
        validation_payload = {'Hello': 'WORLD!'}
        self.assertEqual(
            content,
            validation_payload,
            f"Expected {validation_payload} but got {content}",
        )

    def test_home(self):
        resp, content = call(
            "get",
            f"{TEST_URI}/home",
            assert_code=200,
        )
        validation_payload = {'Hello': 'WORLD!'}
        self.assertEqual(
            content,
            validation_payload,
            f"Expected {validation_payload} but got {content}",
        )

    def test_favicon(self):
        resp, content = call(
            "get",
            f"{TEST_URI}/favicon.ico",
            assert_code=200,
        )

    def test_robots(self):
        resp, content = call(
            "get",
            f"{TEST_URI}/robots.txt",
            assert_code=200,
        )

    # def test_about(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/",
    #         assert_code=200,
    #     )
    #     validation_payload = {'Hello': 'WORLD!'}
    #     self.assertEqual(
    #         content,
    #         validation_payload,
    #         f"Expected {validation_payload} but got {content}",
    #     )

    # def test_service_info(self):
    #     resp, content = call(
    #         "get",
    #         f"{TEST_URI}/",
    #         assert_code=200,
    #     )
    #     validation_payload = {'Hello': 'WORLD!'}
    #     self.assertEqual(
    #         content,
    #         validation_payload,
    #         f"Expected {validation_payload} but got {content}",
    #     )
