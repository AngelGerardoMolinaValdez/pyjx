from models.issue_base import IssueBase

class TestSet(IssueBase):
    """Representa un issue tipo "Test Set".

    Contiene métodos para obtener la información de los tests de su contenido. Un metodo para agregar un o mas tests y uno mas para removerlos.
    """

    def __init__(self, details: dict, factory):
        super().__init__(details, factory)
        self.__tests = None

    def tests(self):
        """Devuelve los tests asociados al Test Set.

        Returns:
            list: Una lista de tests asociados al Test Set.

        Examples:
            >>> test_set.tests()
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
    
    def test_keys(self):
        """Devuelve las claves de los tests asociados al Test Set.

        Returns:
            list: Una lista de claves de tests asociados al Test Set.

        Examples:
            >>> test_set.test_keys()
            ["PJX-1", "PJX-2"]
        """
        return [test.key() for test in self.tests()]

    def test_count(self):
        """Devuelve la cantidad de tests asociados al Test Set.

        Returns:
            int: La cantidad de tests asociados al Test Set.

        Examples:
            >>> test_set.test_count()
            2
        """
        return len(self.__tests)

    def __set_tests(self):
        response_json = self.__client.get(f"rest/raven/1.0/api/testset/{self.key()}/test")
        self.__tests = self.__factory.bulk_get([test["key"] for test in response_json])

    def add(self, test_keys: list[str]):
        """Agrega tests al Test Set.
        
        Args:
            test_keys (list[str]): Una lista de claves de tests a agregar.
            
        Examples:
            >>> test_set.add(["PJX-1", "PJX-2"])
        """
        data = {
            "add": test_keys
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        self.__client.post(f"rest/raven/1.0/api/testset/{self.key()}/test", json=data, headers=headers)
        self.__set_tests()

    def remove(self, test_keys: list[str]):
        """Remueve tests del Test Set.

        Args:
            test_keys (list[str]): Una lista de claves de tests a remover.

        Examples:
            >>> test_set.remove(["PJX-1", "PJX-2"])
        """
        data = {
            "remove": test_keys
        }
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        self.__client.post(f"rest/raven/1.0/api/testset/{self.key()}/test", json=data, headers=headers)
        self.__set_tests()

    def __repr__(self) -> str:
        return f"TestSet(key={self.key()}, summary={self.summary()}, tests={self.test_count()})"
