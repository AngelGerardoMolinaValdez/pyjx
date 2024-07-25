import os
import json
from jsonschema import validate
from pyjx.api.factories.issue_factory import IssueFactory
from pyjx.api.client import Client
from pyjx.api.builders.requests.create import RequestBodyCreateBuilder
from pyjx.config.global_config import GlobalConfig
from pyjx.observers.console_env_report_observer import ConsoleEnvReportObserver
from pyjx.observers.text_env_report_observer import TextEnvReportObserver
from .strategies.add_strategy import TestAdditionStrategy
from .strategies.clone_strategy import TestClonationStrategy
from .strategies.create_strategy import TestCreationStrategy


class EnvironmentCommand:
    def __init__(self, args, invoke_path: str) -> None:
        self.__global_config = GlobalConfig
        self.__args = args
        self.__invoke_path = invoke_path
        path = args.path if args.path is not None else os.path.join(invoke_path, args.namespace)
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schemas", "environment_schema_" + str(args.schema_version) + ".json"))

        if not os.path.exists(path):
            raise FileNotFoundError("No fue encontrado el esquema para la ejecución de ambientación. Verifique la ruta del archivo.")

        with open(path, mode="r", encoding="utf-8") as json_file:
            content: dict = json.load(json_file)

        with open(schema_path, mode="r", encoding="utf-8") as json_schema_file:
            schema = json.load(json_schema_file)

        validate(content, schema)

        global_auth = self.__global_config.get_auth()

        if content.get("auth"):
            self.__auth: dict = content.get("auth")
        elif global_auth is not None:
            self.__auth = global_auth
        else:
            raise ValueError("No hay datos para la autenticación. Configure la propiedad 'auth' o defina sus credenciales con `pyjx2 config auth`")

        self.__data = content
    
    def execute(self):
        Client.configure_auth(**self.__auth)

        test_plan_key = self.__data.get("plan")
        test_execution_key = self.__data.get("execution")
        test_set_key = self.__data.get("set")

        add_fields = self.__data.get("tests", {}).get("add", None)
        clone_fields = self.__data.get("tests", {}).get("clone", None)
        create_fields = self.__data.get("tests", {}).get("create", None)
        tests_fields = self.__data.get("tests", {}).get("fields", None)

        issue_creator = IssueFactory()

        if self.__args.txt_report:
            issue_creator.register_observer(TextEnvReportObserver(self.__invoke_path))

        if not self.__args.no_console_report:
            issue_creator.register_observer(ConsoleEnvReportObserver())

        issue_test_plan = issue_creator.get(test_plan_key)

        test_plan_summary: str = ""
        test_plan_domain: str = ""
        test_plan_celula: str = ""
        test_plan_org: str = ""

        request_body_builder = RequestBodyCreateBuilder()

        if test_execution_key is None:
            execution_body = request_body_builder.add_summary("").add_issue_type("Test Execution").build()
            issue_test_execution = issue_creator.create(execution_body)
            request_body_builder.reset()
        else:
            issue_test_execution = issue_creator.get(test_execution_key)
            
        if test_set_key is None:
            set_body = request_body_builder.add_summary("").add_issue_type("Test Set").build()
            issue_test_set = issue_creator.create(set_body)
            request_body_builder.reset()
        else:
            issue_test_set = issue_creator.get(test_set_key)

        add_strategy = TestAdditionStrategy()
        add_strategy.operation(add_fields, issue_test_set, issue_creator)

        clone_strategy = TestClonationStrategy()
        clone_strategy.operation(clone_fields, tests_fields, issue_test_set, issue_creator)

        creation_strategy = TestCreationStrategy()
        creation_strategy.operation(create_fields, tests_fields, issue_test_set, issue_creator)
        
        issue_test_execution.add([issue_test_set.key()])
        issue_test_plan.add([issue_test_execution.key()])
