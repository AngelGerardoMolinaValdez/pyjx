from json import dumps
from api.client import Client
from abc import ABC

class IssueBase(ABC):
    def __init__(self, fields: dict, factory, observers) -> None:
        """Inicializa una nueva instancia de IssueBase.

        Args:
            fields (dict): Un diccionario con los campos del Issue.
        """
        self.__fields = fields
        self.__client = Client
        self.__factory = factory
        self.__observers = observers
        self.__issue_deleted = False

    def key(self) -> str:
        """Devuelve la clave del Issue.

        Returns:
            str: La clave del Issue.

        Examples:
            >>> issue.key()
            "PJX-1"
        """
        return self.__fields.get("key")

    def issuetype(self) -> str:
        """Devuelve el tipo del Issue.

        Returns:
            str: La clave del Issue.

        Examples:
            >>> issue.issuetype()
            "PJX-1"
        """
        return self.__fields.get("fields", {}).get("issuetype", {}).get("name", {})

    def id(self) -> str:
        """Devuelve el id del Issue.

        Returns:
            str: El id del Issue.

        Examples:
            >>> issue.id()
            "123131"
        """
        return str(self.__fields.get("id"))

    def summary(self) -> str:
        """Devuelve el resumen del Issue.

        Returns:
            str: El resumen del Issue.

        Examples:
            >>> issue.summary()
            "This is a summary"
        """
        return self.__fields.get("fields", {}).get("summary", None)
    
    def json(self) -> dict:
        """Devuelve los campos del Issue obtenidos de la API de Jira.

        Returns:
            dict: Los campos del Issue.

        Examples:
            >>> issue.json()
            {
                "key": "PJX-1",
                "summary": "This is a summary",
                "description": "This is a description"
            }
        """
        return self.__fields

    def url(self) -> str:
        """Devuelve la URL del Issue.

        Returns:
            str: La URL del Issue donde se puede ver en Jira.

        Examples:
            >>> issue.url()
            "https://jira.com/browse/PJX-1"
        """
        return self.__fields.get("self")

    def update(self, fields: dict) -> None:
        """Actualiza los campos del Issue.

        Args:
            fields (dict): Un diccionario con los campos a actualizar.

        Examples:
            >>> issue.update({
                "fields": {
                    "summary": "This is a new summary",
                    "description": "This is a new description"
                }
            })
        """
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        self.__client.put(f"rest/api/2/issue/{self.key()}", data=dumps(fields), headers=headers)
        self.__update_fields(fields)

    def delete(self) -> None:
        """Elimina el Issue.
        
        Examples:
            >>> issue.delete()
        """
        self.__client.delete(f"rest/api/2/issue/{self.key()}")
        self.__issue_deleted = True
    
    def exists(self) -> bool:
        """Verifica si el Issue existe en Jira.

        Returns:
            bool: True si el Issue existe, False en caso contrario.

        Examples:
            >>> issue.exists()
            True
        """
        return not self.__issue_deleted

    def __update_fields(self, new_fields: dict) -> None:
        self.__fields.update(new_fields)

    def __str__(self) -> str:
        return str(self.key())
