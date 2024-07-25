import os
import unittest
import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from assertpy import assert_that

class TestJSONSchemaEnv(unittest.TestCase):

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
                'environment_schema_1.json'
            )
        )
        with open(path, 'r', encoding="utf-8") as file:
            cls.schema = json.load(file)

    def test_simple_json_clone_valid(self):
        fields = {
            "plan": "PJX-65",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": [
                        "PJX-654",
                        "PJX-64"
                    ]
                },
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"}
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_plan_valid_key(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                },
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"}
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_plan_invalid_key_format(self):
        fields = {
            "plan": "PJX-654 ",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_execution_valid_key(self):
        fields = {
            "plan": "PJX-6",
            "execution": "PJX-65476",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "keys": ["PJX-654646646"],
                    "clone": True
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_execution_invalid_key_format(self):
        fields = {
            "plan": "PJX-657",
            "execution": "pjx-6454",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "execution": "PYJX-676"
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_set_valid_key(self):
        fields = {
            "plan": "PJX-6",
            "set": "PJX-6465464564654",
            "execution": "PJX-65",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "plan": "PJX-646",
                    "clone": True
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()


    def test_set_invalid_key_format(self):
        fields = {
            "plan": "PJX-6",
            "set": "pjx-6465464564654",
            "execution": "PJX-65",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "plan": "PJX-646",
                    "clone": True
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_add_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_clone_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                },
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"}
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_create_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "create": [
                    "Test 1",
                    "Test 2"
                ],
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"}
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_clone_missing_fields(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_clone_with_fields_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                },
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"}
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_clone_with_fields_invalid_app_key(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                },
                "fields": {
                    "app": {"key": "INVALID-654"}
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_clone_with_labels(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "clone": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                },
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"},
                    "labels": ["label1", "label2"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_fields_app_valid_key(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"}
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_fields_app_missing_key(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "fields": {
                    "app": {}
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_fields_labels_unique_items(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "fields": {
                    "path": "path/to/tests/to/clone",
                    "app": {"key": "CDA-654"},
                    "labels": ["label1", "label2"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_test_action_properties_path_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_test_action_properties_keys_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_test_action_properties_keys_invalid_format(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "keys": ["INVALID-64"]
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_test_action_properties_execution_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "execution": "PJX-654",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_test_action_properties_execution_invalid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "execution": "INVALID-654",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_test_action_properties_set_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "set": "PJX-654",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_test_action_properties_set_invalid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "set": "INVALID-654",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)

    def test_test_action_properties_plan_valid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "plan": "PJX-654",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate(fields, self.schema)).is_none()

    def test_test_action_properties_plan_invalid(self):
        fields = {
            "plan": "PJX-654",
            "tests": {
                "add": {
                    "path": "path/to/tests",
                    "plan": "INVALID-654",
                    "keys": ["PJX-64"]
                }
            }
        }
        assert_that(validate).raises(ValidationError).when_called_with(fields, self.schema)
