from models.issue_base import IssueBase

class Test(IssueBase):
    """Representa un issue tipo "Test".

    Contiene métodos para obtener la información de los tests de su contenido.
    """

    def __init__(self, details: dict, factory):
        super().__init__(details, factory)
        self.__test_execution_key = None
        self.__test_run_id = None
        self.__test_execution_status = "NotDefined"
    
    def set_test_execution_key(self, key: str) -> None:
        """Establece la clave de ejecución del Test.
        
        Args:
            key (str): La clave de ejecución del Test.
            
        Examples:
            >>> test.set_test_execution_key("PJX-1")
        """
        self.__test_execution_key = key
    
    def test_execution_key(self) -> str:
        """Devuelve la clave de ejecución del Test.

        Returns:
            str: La clave de ejecución del Test.
        """
        return self.__test_execution_key

    def set_test_set_key(self, key: str) -> None:
        """Establece la clave de ejecución del Test.
        
        Args:
            key (str): La clave de ejecución del Test.
            
        Examples:
            >>> test.set_test_set_key("PJX-1")
        """
        self.__test_set_key = key
    
    def test_set_key(self) -> str:
        """Devuelve la clave de ejecución del Test.

        Returns:
            str: La clave de ejecución del Test.
        """
        return self.__test_set_key

    def set_test_plan_key(self, key: str) -> None:
        """Establece la clave de ejecución del Test.
        
        Args:
            key (str): La clave de ejecución del Test.
            
        Examples:
            >>> test.set_test_plan_key("PJX-1")
        """
        self.__test_plan_key = key
    
    def test_plan_key(self) -> str:
        """Devuelve la clave de ejecución del Test.

        Returns:
            str: La clave de ejecución del Test.
        """
        return self.__test_plan_key

    def set_test_run_id(self, id_: dict) -> None:
        """Establece los datos del test run en el Test.
        
        Args:
            id_ (dict): Un diccionario con los datos del test run.
            
        Examples:
            >>> test_run.set_test_run_data(123131)
        """
        self.__test_run_id = id_

    def test_run_id(self) -> int:
        """Devuelve el ID del test run del Test.

        Returns:
            int: El ID del test run.
        """
        return self.__test_run_id
    
    def test_run_status(self) -> str:
        """Devuelve el estado de la ejecución del Test.

        Returns:
            str: El estado de la ejecución del Test.
        """
        return self.__test_execution_status

    def set_test_run_status(self, status: str) -> None:
        """Establece el estado de la ejecución del Test.

        Args:
            status (str): El estado de la ejecución del Test.
        """
        self.__test_execution_status = status

    def __repr__(self) -> str:
        return f"Test(key={self.key()}, test_execution={self.__test_execution_key}, test_run={self.__test_run_data.get("id", "NotDefined")}, status={self.__test_execution_status}, summary={self.summary()})"
