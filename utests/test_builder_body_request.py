from unittest import TestCase
from assertpy import assert_that

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..', "src", "pyjx")))

from api.builders.requests.create import RequestBodyCreateBuilder
from api.builders.requests.bulk_create import RequestBodyBulkCreateBuilder


class TestsBuilderBodyRequest(TestCase):
    def test_create(self):
        builder = RequestBodyCreateBuilder()
        builder.add_issue_type("Test")
        builder.add_summary("UTest 1 creado desde pruebas unitarias.")
        body = builder.build()
        assert_that(body).is_equal_to({
            "fields": {
                "summary": "UTest 1 creado desde pruebas unitarias.",
                "issuetype": {"name": "Test"},
                "project": {"key": "PJX"},
            }
        })
    
    def test_create_without_project(self):
        builder = RequestBodyCreateBuilder(add_project=False)
        builder.add_issue_type("Test")
        builder.add_summary("UTest 1 creado desde pruebas unitarias.")
        body = builder.build()
        assert_that(body).is_equal_to({
            "fields": {
                "summary": "UTest 1 creado desde pruebas unitarias.",
                "issuetype": {"name": "Test"}
            }
        })
    
    def test_bulk_create(self):
        builder = RequestBodyCreateBuilder()
        builder.add_issue_type("Test")
        builder.add_summary("UTest 1 creado desde pruebas unitarias.")
        body = builder.build()

        bulk_builder = RequestBodyBulkCreateBuilder()
        bulk_builder.add_issue(body)
        bulk_body = bulk_builder.build()

        assert_that(bulk_body).is_equal_to({
            "issueUpdates": [
                {
                    "fields": {
                        "summary": "UTest 1 creado desde pruebas unitarias.",
                        "issuetype": {"name": "Test"},
                        "project": {"key": "PJX"},
                    }
                }
            ]
        })
