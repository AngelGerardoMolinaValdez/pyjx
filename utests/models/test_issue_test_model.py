from unittest import TestCase, SkipTest
import uuid
from requests.auth import HTTPBasicAuth
from assertpy import assert_that
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', "src", "pyjx")))

from api.factories.issue_factory import IssueFactory
from api.client import Client
from models.test import Test

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path)


class TestIssueTestModel(TestCase):
    __factory: IssueFactory = None
    __test: Test = None

    @classmethod
    def setUpClass(cls):
        auth = HTTPBasicAuth(
            os.getenv("JIRA_USERNAME"),
            os.getenv("JIRA_PASSWORD")
        )
        cls.__factory = IssueFactory()
        Client.configure(os.getenv("JIRA_URL"), auth)
        cls.__test = cls.__factory.get("PJX-4")

    def test_issue_summary(self):
        self.__new_test = self.__factory.get("PJX-5")
        assert_that(self.__new_test.summary()).is_equal_to("Test Bulk 1")
    
    def test_issue_key(self):
        assert_that(self.__test.key()).is_equal_to("PJX-4")
    
    def test_issue_id(self):
        assert_that(self.__test.id()).is_equal_to("10026")

    def test_issue_url(self):
        assert_that(self.__test.url()).is_equal_to("https://angelgerardomolinavaldez.atlassian.net/rest/api/2/issue/10026")
    
    def test_issue_json(self):
        assert_that(self.__test.json()).is_instance_of(dict)
    
    def test_issue_update(self):
        _uuid = uuid.uuid4()
        new_name = f"UTest for pyjx {_uuid}"
        self.__test.update({"fields": {"summary": new_name}})
        assert_that(self.__test.summary()).is_equal_to(new_name)
    
    def test_issue_delete(self):
        new_issue = self.__factory.create(
            {
                "fields": {
                    "summary": "This is a summary",
                    "description": "This is a description",
                    "issuetype": {"name": "Test"},
                    "project": {"key": "PJX"}
                }
            }
        )
        new_issue.delete()
        assert_that(new_issue.exists()).is_false()
    
    def test_run_id(self):
        self.__test.set_test_run_id(123131)
        assert_that(self.__test.test_run_id()).is_equal_to(123131)
    
    def test_run_status(self):
        self.__test.set_test_run_status("PASSED")
        assert_that(self.__test.test_run_status()).is_equal_to("PASSED")
    
    def test_execution_key(self):
        self.__test.set_test_execution_key("PJX-1")
        assert_that(self.__test.test_execution_key()).is_equal_to("PJX-1")

    def test_set_key(self):
        self.__test.set_test_set_key("PJX-1")
        assert_that(self.__test.test_set_key()).is_equal_to("PJX-1")
    
    def test_plan_key(self):
        self.__test.set_test_plan_key("PJX-1")
        assert_that(self.__test.test_plan_key()).is_equal_to("PJX-1")
