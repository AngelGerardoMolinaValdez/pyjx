from typing import Union
from pyjx.api.factories.issue_factory import IssueFactory
from models.issue_base import IssueBase
from pyjx.api.builders.requests.create import RequestBodyCreateBuilder
from pyjx.api.builders.requests.bulk_create import RequestBodyBulkCreateBuilder


class TestCreationStrategy:
    def operation(self, fields: Union[list, None],  tests_fields: Union[dict, None], issue: IssueBase, factory: IssueFactory) -> None:
        if fields is None:
            return

        bulk_create_builder = RequestBodyBulkCreateBuilder()

        for issue_name in fields:
            create_builder = RequestBodyCreateBuilder()
            body = create_builder.add_summary(issue_name).add_issue_type("Test").build()
            bulk_create_builder.add_issue(body)

        bulk_data = bulk_create_builder.build()
        tests = factory.bulk_create(bulk_data)
        issue.add([test.key for test in tests])
