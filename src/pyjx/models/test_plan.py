from models.issue_base import IssueBase

class TestPlan(IssueBase):
    def __init__(self, details: dict, factory):
        super().__init__(details, factory)
        self.__tests = None
        self.__test_executions = None
    
    def tests(self) -> list:
        """Devuelve los tests asociados al Test Plan.

        Returns:
            list: Una lista de tests asociados al Test Plan.

        Examples:
            >>> test_plan.tests()
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
        response_json = self.__client.get(f"rest/raven/1.0/api/testplan/{self.key()}/test")
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

    def test_executions(self) -> list:
        """Devuelve los test executions asociados al Test Plan.

        Returns:
            list: Una lista de test executions asociados al Test Plan.

        Examples:
            >>> test_plan.test_executions()
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
        self.__set_test_executions()
        return self.__test_executions

    def __set_test_executions(self):
        response_json = self.__client.get(f"rest/raven/1.0/api/testplan/{self.key()}/testexecution")
        self.__test_executions = self.__factory.bulk_get([test["key"] for test in response_json])

    def test_execution_keys(self):
        """Devuelve las claves de los tests asociados al Test Set.

        Returns:
            list: Una lista de claves de tests asociados al Test Set.

        Examples:
            >>> test_set.test_keys()
            ["PJX-1", "PJX-2"]
        """
        return [test.key() for test in self.test_executions()]

    def add_test_executions(self, test_execution_keys: dict) -> None:
        """Agrega test executions al Test Plan.

        Args:
            test_execution_keys (dict): Un diccionario con las claves de los test executions a agregar.

        Examples:
            >>> test_plan.add_test_executions({"add": ["PJX-1", "PJX-2"]})
        """
        data = {
            "addTestsToPlan": True,
            "add": test_execution_keys
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        self.__client.post(f"rest/raven/1.0/api/testplan/{self.key()}/testexecution", json=data, headers=headers)
        self.test_executions()
    
    def remove_test_executions(self, test_execution_keys: dict) -> None:
        """Remueve test executions del Test Plan.

        Args:
            test_execution_keys (dict): Un diccionario con las claves de los test executions a remover.

        Examples:
            >>> test_plan.remove_test_executions({"remove": ["PJX-1", "PJX-2"]})
        """
        data = {
            "remove": test_execution_keys
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
        self.__client.post(f"rest/raven/1.0/api/testplan/{self.key()}/testexecution", json=data, headers=headers)
        self.test_executions()
    
    def test_count(self) -> int:
        """Devuelve la cantidad de tests asociados al Test Plan.

        Returns:
            int: La cantidad de tests asociados al Test Plan.

        Examples:
            >>> test_plan.test_count()
            2
        """
        return len(self.__tests)
    
    def test_execution_count(self) -> int:
        """Devuelve la cantidad de test executions asociados al Test Plan.

        Returns:
            int: La cantidad de test executions asociados al Test Plan.

        Examples:
            >>> test_plan.test_execution_count()
            2
        """
        return len(self.__set_test_executions)

    def __repr__(self) -> str:
        return f"TestPlan(key={self.key()}, summary={self.summary()})"
