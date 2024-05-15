from typing import Union
from json import dumps
from models.test import Test
from models.test_set import TestSet
from models.test_execution import TestExecution
from models.test_plan import TestPlan
from api.client import Client

class IssueFactory:
    """Clase de fábrica para la creación y gestión de instancias de Test.

    Esta clase facilita la creación, clonación y recuperación de instancias de variedad de issues
    utilizando llamadas  a la API REST de JIRA.

    Atributos:
        __issue_types (dict): Un diccionario que mapea los tipos de issues a sus respectivas clases.

    Métodos:
        create(details): Crea una nueva instancia de un issue de Jira.
        bulk_create(details): Crea múltiples nuevas instancias de Issues de Jira.
        clone(issue_key, details): Clona una instancia de un issue de Jira.
        bulk_clone(data): Clona múltiples instancias de issues de Jira.
        get(key_or_id): Obtiene una instancia de un issue de Jira por su clave o ID.
        bulk_get(keys_or_ids): Obtiene múltiples instancias de issues de Jira por sus claves o IDs.
        get_tests_from_test_repository(test_repository_id): Obtiene los tests asociados a un Test Repository.
        get_issues_from_summary(summary, type_issue): Obtiene los issues según el summary y el tipo de issue.
        get_issues_from_summaries(summaries, type_issue): Obtiene los issues según los summaries y el tipo de issue.
    """
    __issue_types = {
        "Test": Test,
        "Test Execution": TestSet,
        "Test Plan": TestSet,
        "Test Set": TestSet
    }

    def __init__(self) -> None:
        """Inicializa la TestFactory con un cliente API."""
        self.__client = Client

    def create(self, details: dict) -> Union[Test, TestSet, TestExecution, TestPlan]:
        """Crea una nueva instancia de un issue de Jira.

        Args:
            details (dict): Un diccionario con los detalles del issue a crear.

        Returns:
            Union[Test, TestSet, TestExecution, TestPlan]: La instancia del issue creado.
        
        Examples:
            >>> issue_factory.create({
                "fields": {
                    "summary": "This is a summary",
                    "description": "This is a description"
                }
            })
        """
        response = self.__client.post("rest/api/2/issue", json=details)
        issue = self.get(response["key"])

        return issue

    def bulk_create(self, details: dict) -> list[Union[Test, TestSet, TestExecution, TestPlan]]:
        """Crea múltiples nuevas instancias de Issues de Jira.

        Args:
            details (dict): Un diccionario que contiene listas de detalles para cada Issue.

        Returns:
            list: Lista de instancias de Issues creadas.
        
        Examples:
            >>> issue_factory.bulk_create({
                "issueUpdates": [
                    {
                        "fields": {
                            "summary": "This is a summary"
                        }
                    },
                    {
                        "fields": {
                            "summary": "This is another summary"
                        }
                    }
                ]
            })
        """
        def __create_issue(data: dict) -> Test:
            issue = self.get(data["key"])

            return issue

        response = self.__client.post("rest/api/2/issue/bulk", json=details)
        issues = list(map(__create_issue, response["issues"]))

        return issues

    def clone(self, issue_key: str, details: dict) -> Union[Test, TestSet, TestExecution, TestPlan]:
        """Clona una instancia de un issue de Jira.

        Args:
            issue_key (str): La clave de la instancia del issue a clonar.
            details (dict): Detalles para el nuevo issue clonado.

        Returns:
            Union[Test, TestSet, TestExecution, TestPlan]: La instancia del issue clonado.

        Examples:
            >>> issue_factory.clone("PJX-1", {
                "fields": {
                    "summary": "This is a summary"
                }
            })
        """
        response_new_issue = self.__client.post("rest/api/2/issue", json=details)
        new_issue = self.get(response_new_issue["key"])

        issue_link_data = {
            "type": {"name": "Duplicate"},
            "inwardIssue": {"key": issue_key},
            "outwardIssue": {"key": new_issue.key()}
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        self.__client.post("rest/api/2/issueLink", data=dumps(issue_link_data), headers=headers)

        return new_issue

    def bulk_clone(self, data: dict[str, dict]) -> list[Union[Test, TestSet, TestExecution, TestPlan]]:
        """Clona múltiples instancias de issues de Jira.

        Args:
            data (dict): Un diccionario que mapea las claves de los issues a sus respectivos detalles.

        Returns:
            list: Lista de instancias de issues clonados.
        
        Examples:
            >>> issue_factory.bulk_clone({
                "PXJ-1": {
                    "fields": {
                        "summary": "This is a summary"
                    }
                },
                "PXJ-2": {
                    "fields": {
                        "summary": "This is another summary"
                    }
                }
            })
        """
        issue_details = [details for key, details in data.items()]
        
        new_issues = self.bulk_create({"issueUpdates": issue_details})

        for index, (key, content) in enumerate(data.items()):
            issue_link_data = {
                "type": {"name": "Duplicate"},
                "inwardIssue": {"key": key},
                "outwardIssue": {"key": new_issues[index].key()}
            }
            headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
            self.__client.post("rest/api/2/issueLink", data=dumps(issue_link_data), headers=headers)

        return new_issues

    def get(self, key_or_id: str) -> Union[Test, TestSet, TestExecution, TestPlan]:
        """Obtiene una instancia de un issue de Jira por su clave o ID.

        Args:
            key_or_id (str): La clave o ID del issue a recuperar.

        Returns:
            Union[Test, TestSet, TestExecution, TestPlan]: La instancia del issue recuperado.
        
        Examples:
            >>> issue_factory.get("PJX-1")
        """
        response = self.__client.get(f"rest/api/2/issue/{key_or_id}")
        Issue = self.__issue_types[response["fields"]["issuetype"]["name"]]

        return Issue(response, self)

    def bulk_get(self, keys_or_ids: list[str]) -> list[Union[Test, TestSet, TestExecution, TestPlan]]:
        """Obtiene múltiples instancias de issues de Jira por sus claves o IDs.

        Args:
            keys_or_ids (list): Lista de claves o IDs de los issues a recuperar.

        Returns:
            list: Lista de instancias de issues recuperados.
        
        Examples:
            >>> issue_factory.bulk_get(["PJX-1", "PJX-2"])
        """
        params = {
            "jql": f"id in ({','.join(keys_or_ids)})"
        }

        response = self.__client.get("rest/api/2/search", params=params)

        return [self.get(details["key"]) for details in response["issues"]]

    def get_tests_from_test_repository(self, test_repository_id: str) -> list[Test]:
        """Obtiene los tests asociados a un Test Repository.

        Args:
            test_repository_id (str): La clave del Test Repository.

        Returns:
            list: Lista de instancias de Test asociadas al Test Repository.
        
        Examples:
            >>> issue_factory.get_tests_from_test_repository(12312)
            [
                {
                    "key": "PJX-1",
                    "summary": "This is a summary"
                },
                {
                    "key": "PJX-2",
                    "summary": "This is another summary"
                }
            ]
        """
        response_json = self.__client.get(f"rest/raven/1.0/api/testrepository/PJX/folders/{str(test_repository_id)}/tests")
        keys = [test_info["key"] for test_info in response_json["tests"]]
        tests_from_tr = self.bulk_get(keys)

        return tests_from_tr

    def get_issues_from_summary(self, summary: str, type_issue: str) -> list[Union[Test, TestSet, TestExecution, TestPlan]]:
        """Obtiene los issues segun el summary y el tipo de issue.

        Considerar que solo obtendrá los issues que tengan el mismo tipo de issue.
        
        Args:
            summary (str): El resumen del issue.
            type_issue (str): El tipo de issue.
            
        Returns:
            list: Lista de instancias de issues
            
        Examples:
            >>> issue_factory.get_issues_from_summary("This is a summary", "Test")
            [
                {
                    "key": "PJX-1",
                    "summary": "This is a summary"
                },
                {
                    "key": "PJX-2",
                    "summary": "This is another summary"
                }
            ]
        """
        params = {
            "jql": f'project = "PJX" AND summary ~ "{summary}" AND issuetype = "{type_issue}"'
        }
        response = self.__client.get("rest/api/2/search", params=params)
        keys = [test_info["key"] for test_info in response["issues"]]
        issues = self.bulk_get(keys)

        return issues
    
    def get_issues_from_summaries(self, summaries: list[str], type_issue: str) -> list[Union[Test, TestSet, TestExecution, TestPlan]]:
        """Obtiene los issues según los summaries y el tipo de issue.
        
        Considerar que solo obtendrá los issues que tengan el mismo tipo de issue.

        Args:
            summaries (list[str]): Lista de resúmenes de los issues.
            type_issue (str): El tipo de issue.
            
        Returns:
            list: Lista de instancias de issues
            
        Examples:
            >>> issue_factory.get_issues_from_summaries(["This is a summary", "This is another summary"], "Test")
            [
                {
                    "key": "PJX-1",
                    "summary": "This is a summary"
                },
                {
                    "key": "PJX-2",
                    "summary": "This is another summary"
                }
            ]
        """
        jql_query = " OR ".join([f'summary ~ "{summary}"' for summary in summaries])
        params = {
            "jql": f'{jql_query} AND issuetype = "{type_issue}"'
        }

        response = self.__client.get("rest/api/2/search", params=params)
        keys = [test_info["key"] for test_info in response["issues"]]

        issues = self.bulk_get(keys)

        return issues
