from typing import Self

class RequestBodyCreateBuilder:
    """
    Una clase constructora para crear un body request para crear un issue en Jira.

    Atributos
    ----------
    __fields : dict
        Un diccionario que representa los campos del problema.

    Métodos
    -------
    __init__(self, add_project: bool = True) -> None:
        Inicializa el RequestBodyCreateBuilder. Si add_project es True, se agrega un proyecto predeterminado con la clave "PJX".

    add_project(self, project: str) -> Self:
        Agrega un proyecto a los campos. El proyecto se representa por su clave.

    add_summary(self, summary: str) -> Self:
        Agrega un resumen a los campos.

    add_issuetype(self, issuetype: str) -> Self:
        Agrega un tipo de problema a los campos. El tipo de problema se representa por su nombre.

    add_description(self, description: str) -> Self:
        Agrega una descripción a los campos.

    add_labels(self, labels: list) -> Self:
        Agrega etiquetas a los campos.

    build(self, body: dict) -> dict:
        Construye y devuelve el cuerpo de la solicitud.
    """
    def __init__(self, add_project: bool = True) -> None:
        if add_project:
            project = {"project": {"key": "PJX"}}
        else:
            project = {}

        self.__fields = {
            "fields": project
        }

    def add_project(self, project: str) -> Self:
        """Agrega un proyecto a los campos.
        
        Args:
            project (str): La clave del proyecto.
            
        Returns:
            Self: El objeto RequestBodyCreateBuilder.
        
        Examples:
            >>> builder.add_project("PJX")
        """
        self.__fields["fields"]["project"] = {"key": project}
        return self

    def add_summary(self, summary: str) -> Self:
        """Agrega un resumen a los campos.

        Args:
            summary (str): El resumen del problema.
        
        Returns:
            Self: El objeto RequestBodyCreateBuilder.
        
        Examples:
            >>> builder.add_summary("This is a summary")
        """
        self.__fields["fields"]["summary"] = summary
        return self
    
    def add_issue_type(self, issuetype: str) -> Self:
        """Agrega un tipo de problema a los campos.

        Args:
            issuetype (str): El nombre del tipo de problema.

        Returns:
            Self: El objeto RequestBodyCreateBuilder.
        
        Examples:
            >>> builder.add_issuetype("Task")
        """
        self.__fields["fields"]["issuetype"] = {"name": issuetype}
        return self
    
    def add_description(self, description: str) -> Self:
        """Agrega una descripción a los campos.

        Args:
            description (str): La descripción del problema.
        
        Returns:
            Self: El objeto RequestBodyCreateBuilder.
        
        Examples:
            >>> builder.add_description("This is a description")
        """
        self.__fields["fields"]["description"] = description
        return self
    
    def add_labels(self, labels: list) -> Self:
        """Agrega etiquetas a los campos.

        Args:
            labels (list): Una lista de etiquetas.

        Returns:
            Self: El objeto RequestBodyCreateBuilder.
        
        Examples:
            >>> builder.add_labels(["label1", "label2"])
        """
        self.__fields["fields"]["labels"] = labels
        return self
    
    def build(self) -> dict:
        """Construye y devuelve el cuerpo de la solicitud.

        Args:
            body (dict): Un diccionario con los campos del problema.
        
        Returns:
            dict: El cuerpo de la solicitud.
        
        Examples:
            >>> builder.build()
            {
                "fields": {
                    "project": {"key": "PJX"},
                    "summary": "This is a summary",
                    "issuetype": {"name": "Task"},
                    "description": "This is a description",
                    "labels": ["label1", "label2"]
                }
            }
        """
        return self.__fields
