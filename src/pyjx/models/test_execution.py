from models.issue_base import IssueBase
from models.test import Test

class TestExecution(IssueBase):
    def __init__(self, details: dict, factory):
        super().__init__(details, factory)
        self.__tests = None

    def tests(self):
        """Devuelve los tests asociados al Test Execution.

        Returns:
            list: Una lista de tests asociados al Test Execution.

        Examples:
            >>> test_execution.tests()
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
        self.__set_tests()
        return self.__tests

    def __set_tests(self):
        response_json = self.__client.get(f"rest/raven/1.0/api/testexec/{self.key()}/test")
        self.__tests = self.__factory.bulk_get([test["key"] for test in response_json])

    def test_keys(self):
        """Devuelve las claves de los tests asociados al Test Set.

        Returns:
            list: Una lista de claves de tests asociados al Test Set.

        Examples:
            >>> test_set.test_keys()
            ["PJX-1", "PJX-2"]
        """
        return [test.key() for test in self.__tests]

    def add(self, issue_keys: list[str]) -> None:
        """Agrega tests al Test Execution.

        Args:
            issue_keys (list[str]): Una lista de claves de tests a agregar.

        Examples:
            >>> test_execution.add(["PJX-1", "PJX-2"])
        """
        data = {
            "add": issue_keys
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        response_json = self.__client.post(f"rest/raven/1.0/api/testexec/{self.key()}/test", json=data, headers=headers)
        self.__set_tests()

        return response_json

    def remove(self, issue_keys: list[str]) -> None:
        """Remueve tests del Test Execution.
        
        Args:
            issue_keys (list[str]): Una lista de claves de tests a remover.
            
        Examples:
            >>> test_execution.remove(["PJX-1", "PJX-2"])
        """
        data = {
            "remove": issue_keys
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        response_json = self.__client.post(f"rest/raven/1.0/api/testexec/{self.key()}/test", json=data, headers=headers)
        self.__set_tests()

        return response_json

    def test_count(self) -> int:
        """Devuelve la cantidad de tests asociados al Test Execution.

        Returns:
            int: La cantidad de tests asociados al Test Execution.

        Examples:
            >>> test_execution.test_count()
            2
        """
        return len(self.__tests)

    def set_test_status(self, test: Test, status: str) -> None:
        """Establece el estado de los tests en el Test Execution.

        Args:
            test (Test): El test al que se le va a establecer el estado.
            status (str): El estado a establecer en el test.

        Examples:
            >>> test_execution.set_test_status(test, "PASS")
        """
        params = {
            "status": status.upper()
        }
        self.__client.put(f"rest/raven/1.0/api/testrun/{test.test_run_id()}/status", params=params)
        test.set_test_run_status(status)

    def add_attachment_to_test(self, test: Test, attachment_data: dict) -> None:
        """Agrega un archivo adjunto al test dentro del Test Execution.

        Args:
            test (Test): El test al que se le va a agregar el archivo adjunto.
            attachment_data (dict): Un diccionario con los datos del archivo adjunto.

        Examples:
            >>> test_execution.add_attachment(test, {
                "name": "attachment.txt",
                "data": "data",
                contentType: "text/plain"
            })
        """
        self.__client.post(f"rest/raven/1.0/api/testrun/{test.test_run_id()}/attachment", json=attachment_data)

    def __repr__(self) -> str:
        return f"TestExecution(key={self.key()}, summary={self.summary()}, tests={self.test_count()}"
