from unittest import TestCase, SkipTest
from requests.auth import HTTPBasicAuth
from assertpy import assert_that
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', "src", "pyjx")))

from api.factories.issue_factory import IssueFactory
from api.client import Client
from models.test import Test
from models.test_plan import TestPlan

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)


class TestIssueTestPlanModel(TestCase):
    __factory: IssueFactory = None
    __test_plan: TestPlan  = None

    @classmethod
    def setUpClass(cls):
        auth = HTTPBasicAuth(
            os.getenv("JIRA_USERNAME"),
            os.getenv("JIRA_PASSWORD")
        )
        cls.__factory = IssueFactory()
        Client.configure(os.getenv("JIRA_URL"), auth)
        cls.__test_plan = cls.__factory.get("PJX-64")

    @SkipTest
    def test_tests(self):
        tests = self.__test_plan.tests()
        assert_that(tests).is_instance_of(list)
        assert_that(tests[0]).is_instance_of(Test)
    
    @SkipTest
    def test_test_keys(self):
        test_keys = self.__test_plan.test_keys()
        assert_that(test_keys).is_instance_of(list)
        assert_that(test_keys[0]).is_instance_of(str)

    @SkipTest
    def test_test_keys(self):
        test_keys = self.__test_plan.test_execution_keys()
        assert_that(test_keys).is_instance_of(list)
        assert_that(test_keys[0]).is_instance_of(str)

    @SkipTest
    def test_test_count(self):
        test_count = self.__test_plan.test_count()
        assert_that(test_count).is_instance_of(int)
        assert_that(test_count).is_greater_than(0)

    @SkipTest
    def test_test_execution_count(self):
        test_count = self.__test_plan.test_execution_count()
        assert_that(test_count).is_instance_of(int)
        assert_that(test_count).is_greater_than(0)

    @SkipTest
    def test_add_test_execution(self):
        test_keys = ["PJX-69", "PJX-70"]
        self.__test_plan.add_test_executions(test_keys)
        tests = self.__test_plan.test_executions()
        assert_that(tests[0].key()).is_in(test_keys)
        assert_that(tests[1].key()).is_in(test_keys)
    
    @SkipTest
    def test_remove_test_execution(self):
        test_keys = ["PJX-69", "PJX-70"]
        self.__test_plan.remove_test_executions(test_keys)
        tests = self.__test_plan.test_executions()
        assert_that(tests[0].key()).is_not_in(test_keys)
        assert_that(tests[1].key()).is_not_in(test_keys)
