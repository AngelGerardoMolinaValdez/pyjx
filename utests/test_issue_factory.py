from unittest import TestCase, SkipTest
from requests.auth import HTTPBasicAuth
from assertpy import assert_that
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', "src", "pyjx")))

from api.factories.issue_factory import IssueFactory
from api.client import Client
from models.test import Test
from models.test_execution import TestExecution
from models.test_plan import TestPlan
from models.test_set import TestSet

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

class TestIssueFactory(TestCase):
    __factory: IssueFactory = None

    @classmethod
    def setUpClass(cls):
        auth = HTTPBasicAuth(
            os.getenv("JIRA_USERNAME"),
            os.getenv("JIRA_PASSWORD")
        )
        cls.__factory = IssueFactory()
        print(os.getenv("JIRA_URL"), 'validando')
        Client.configure(os.getenv("JIRA_URL"), auth)

    def test_create(self):
        test = self.__factory.create({
            "fields": {
                "summary": "UTest 1 creado desde pruebas unitarias.",
                "issuetype": {"name": "Test"},
                "project": {"key": "PJX"},
            }
        })
        assert_that(test).is_not_none()
        assert_that(test).is_instance_of(Test)

        test_plan = self.__factory.create({
            "fields": {
                "summary": "UTest 1 creado desde pruebas unitarias.",
                "issuetype": {"name": "Test Plan"},
                "project": {"key": "PJX"},
            }
        })
        assert_that(test_plan).is_not_none()
        assert_that(test_plan).is_instance_of(TestSet)

        test_set = self.__factory.create({
            "fields": {
                "summary": "UTest 1 creado desde pruebas unitarias.",
                "issuetype": {"name": "Test Set"},
                "project": {"key": "PJX"},
            }
        })
        assert_that(test_set).is_not_none()
        assert_that(test_set).is_instance_of(TestSet)

        test_execution = self.__factory.create({
            "fields": {
                "summary": "UTest 1 creado desde pruebas unitarias.",
                "issuetype": {"name": "Test Execution"},
                "project": {"key": "PJX"},
            }
        })
        assert_that(test_execution).is_not_none()
        assert_that(test_execution).is_instance_of(TestSet)

    def test_bulk_create(self):
        issues = self.__factory.bulk_create({
            "issueUpdates": [
                {
                    "fields": {
                        "summary": "Bulk Test 1",
                        "issuetype": {"name": "Test"},
                        "project": {"key": "PJX"},
                    }
                },
                {
                    "fields": {
                        "summary": "Bulk Test 2",
                        "issuetype": {"name": "Test"},
                        "project": {"key": "PJX"},
                    }
                },
                {
                    "fields": {
                        "summary": "Bulk Test 3",
                        "issuetype": {"name": "Test Plan"},
                        "project": {"key": "PJX"},
                    }
                },
                {
                    "fields": {
                        "summary": "Bulk Test 4",
                        "issuetype": {"name": "Test Set"},
                        "project": {"key": "PJX"},
                    }
                },
                {
                    "fields": {
                        "summary": "Bulk Test 5",
                        "issuetype": {"name": "Test Execution"},
                        "project": {"key": "PJX"},
                    }
                }
            ]
        })

        assert_that(issues).is_not_empty()
        assert_that(issues).is_length(5)
        assert_that(issues[0]).is_instance_of(Test)
        assert_that(issues[1]).is_instance_of(Test)
        assert_that(issues[2]).is_instance_of(TestSet)
        assert_that(issues[3]).is_instance_of(TestSet)
        assert_that(issues[4]).is_instance_of(TestSet)

    def test_clone(self):
        test_cloned = self.__factory.clone("PJX-65",
                                            {
                                                "fields": {
                                                    "summary": "This is a summary",
                                                    "issuetype": {"name": "Test"},
                                                    "project": {"key": "PJX"}
                                                }
                                            })
        assert_that(test_cloned).is_instance_of(Test)

        test_plan_cloned = self.__factory.clone("PJX-68",
                                                {
                                                    "fields": {
                                                        "summary": "This is a summary",
                                                        "issuetype": {"name": "Test Plan"},
                                                        "project": {"key": "PJX"}
                                                    }
                                                })
        assert_that(test_plan_cloned).is_instance_of(TestSet)

        test_set_cloned = self.__factory.clone("PJX-67",
                                               {
                                                   "fields": {
                                                       "summary": "This is a summary",
                                                       "issuetype": {"name": "Test Set"},
                                                       "project": {"key": "PJX"}
                                                   }
                                               })
        assert_that(test_set_cloned).is_instance_of(TestSet)

        test_execution_cloned = self.__factory.clone("PJX-73",
                                                     {
                                                         "fields": {
                                                             "summary": "This is a summary",
                                                             "issuetype": {"name": "Test Execution"},
                                                             "project": {"key": "PJX"}
                                                         }
                                                     })
        assert_that(test_execution_cloned).is_instance_of(TestSet)

    def test_bulk_clone(self):
        issues = self.__factory.bulk_clone({
            "PJX-69": {
                "fields": {
                    "summary": "This is a summary",
                    "issuetype": {"name": "Test"},
                    "project": {"key": "PJX"}
                }
            },
            "PJX-72": {
                "fields": {
                    "summary": "This is a summary",
                    "issuetype": {"name": "Test Plan"},
                    "project": {"key": "PJX"}
                }
            },
            "PJX-71": {
                "fields": {
                    "summary": "This is a summary",
                    "issuetype": {"name": "Test Set"},
                    "project": {"key": "PJX"}
                }
            },
            "PJX-73": {
                "fields": {
                    "summary": "This is a summary",
                    "issuetype": {"name": "Test Execution"},
                    "project": {"key": "PJX"}
                }
            }
        })

        assert_that(issues).is_not_empty()
        assert_that(issues).is_length(4)
        assert_that(issues[0]).is_instance_of(Test)
        assert_that(issues[1]).is_instance_of(TestSet)
        assert_that(issues[2]).is_instance_of(TestSet)
        assert_that(issues[3]).is_instance_of(TestSet)

    def test_get(self):
        issue = self.__factory.get("PJX-65")
        assert_that(issue).is_instance_of(Test)

        issue = self.__factory.get("PJX-68")
        assert_that(issue).is_instance_of(TestSet)

        issue = self.__factory.get("PJX-67")
        assert_that(issue).is_instance_of(TestSet)

        issue = self.__factory.get("PJX-73")
        assert_that(issue).is_instance_of(TestSet)

    def test_bulk_get(self):
        issues = self.__factory.bulk_get(["PJX-65", "PJX-68", "PJX-67", "PJX-73"])
        assert_that(issues).is_not_empty()
        assert_that(issues).is_length(4)

    @SkipTest
    def test_get_tests_from_test_repository(self):
        tests = self.__factory.get_tests_from_test_repository("1231231")
        assert_that(tests).is_not_empty()

    def test_get_issues_from_summary(self):
        issue = self.__factory.get_issues_from_summary("This is a summary", "Test")
        assert_that(issue[0]).is_instance_of(Test)

        issue = self.__factory.get_issues_from_summary("This is a summary", "Test Plan")
        assert_that(issue[0]).is_instance_of(TestSet)

        issue = self.__factory.get_issues_from_summary("This is a summary", "Test Set")
        assert_that(issue[0]).is_instance_of(TestSet)

        issue = self.__factory.get_issues_from_summary("This is a summary", "Test Execution")
        assert_that(issue[0]).is_instance_of(TestSet)
    
    def test_get_issues_from_summaries(self):
        issues = self.__factory.get_issues_from_summaries(
            ["This is a summary", "UTest 1 creado desde pruebas unitarias.", "Test Bulk 1"], 
            "Test"
        )
        assert_that(issues).is_not_empty()
