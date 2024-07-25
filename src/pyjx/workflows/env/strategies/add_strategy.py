from typing import Union
from pyjx.api.factories.issue_factory import IssueFactory
from models.issue_base import IssueBase


class TestAdditionStrategy:
    def operation(self, fields: Union[dict, None], issue: IssueBase, factory: IssueFactory) -> None:
        if fields is None:
            return

        tests = []

        if (test_plan_key := fields.get("plan")):
            issue_test_plan = factory.get(test_plan_key)
            _tests = issue_test_plan.tests()
            tests += _tests

        if (test_execution_key := fields.get("execution")):
            issue_test_execution = factory.get(test_execution_key)
            _tests = issue_test_execution.tests()
            tests += _tests

        if (test_set_key := fields.get("set")):
            issue_test_set = factory.get(test_set_key)
            _tests = issue_test_set.tests()
            tests += _tests

        if (path_repository_id := fields.get("path")):
            _tests = factory.get_tests_from_test_repository(path_repository_id)
            tests += _tests

        if (test_keys := fields.get("keys")):
            _tests = factory.bulk_get(test_keys)
            tests += _tests

        issue.add([test.key for test in tests])
