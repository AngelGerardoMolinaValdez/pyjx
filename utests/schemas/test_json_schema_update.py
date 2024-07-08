import os
import unittest
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from assertpy import assert_that

class TestJSONSchemaUpdate(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..',
                '..',
                'src',
                'pyjx',
                'schemas',
                'attach_results_schema.json'
            )
        )
        with open(path, 'r', encoding="utf-8") as file:
            cls.schema = json.load(file)    
    
    def test_valid_execution_issue(self):
        fields = {
            "execution": "PJX-654"
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_invalid_execution_issue_format(self):
        fields = {
            "execution": "PJX-65 "
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_status_with_valid_value_and_keys(self):
        fields = {
            "execution": "PJX-654",
            "status": [
                {
                    "value": "PASS",
                    "keys": ["PJX-6", "PJX-65"]
                }
            ]
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_status_with_valid_value_and_set(self):
        fields = {
            "execution": "PJX-654",
            "status": [
                {
                    "value": "PASS",
                    "set": "PJX-67"
                }
            ]
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_status_with_valid_value_and_filter(self):
        fields = {
            "execution": "PJX-654",
            "status": [
                {
                    "value": "PASS",
                    "filter": "path/to/file.py"
                }
            ]
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_status_with_invalid_value(self):
        fields = {
            "execution": "PJX-654",
            "status": [
                {
                    "value": "fail",
                    "keys": ["PJX-6", "PJX-65"]
                }
            ]
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)


    def test_status_missing_required_value(self):
        fields = {
            "execution": "PJX-654",
            "status": [
                {
                    "keys": ["PJX-6", "PJX-65"]
                }
            ]
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_status_with_multiple_filter_types(self):
        fields = {
            "execution": "PJX-654",
            "status": [
                {
                    "value": "PASS",
                    "keys": ["PJX-67", "PJX-6"]
                },
                {
                    "value": "PASS",
                    "set": "PJX-67"
                },
                {
                    "value": "PASS",
                    "filter": "path/to/file.py"
                }
            ]
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_exclude_with_valid_status_array(self):
        fields = {
            "execution": "PJX-654",
            "exclude": {
                "status": ["PASS","FAIL"]
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_exclude_with_invalid_status_value(self):
        fields = {
            "execution": "PJX-654",
            "exclude": {
                "status": ["does not exist","FAIL "]
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_exclude_with_keys(self):
        fields = {
            "execution": "PJX-65",
            "exclude": {
                "keys": ["PJX-6666"]
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_exclude_with_set(self):
        fields = {
            "execution": "PJX-65",
            "exclude": {
                "set": "PJX-6666"
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_exclude_with_filter(self):
        fields = {
            "execution": "PJX-65",
            "exclude": {
                "filter": "path/to/file.py"
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_exclude_with_multiple_filter_types(self):
        fields = {
            "execution": "PJX-65",
            "exclude": {
                "set": "PJX-6666",
                "filter": "path/to/file.py",
                "keys": ["PJX-6666"]
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_missing_required_execution(self):
        fields = {
            "exclude": {
                "set": "PJX-6666",
                "filter": "path/to/file.py",
                "keys": ["PJX-6666"]
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_complete_valid_structure(self):
        fields = {
            "execution": "PJX-65",
            "status": [
                {
                    "value": "FAIL",
                    "filter": "path/to/file.py"
                }
            ],
            "exclude": {
                "keys": ["PJX-6666"]
            }
        }
        assert_that(validate(fields, self.schema)).is_none()
