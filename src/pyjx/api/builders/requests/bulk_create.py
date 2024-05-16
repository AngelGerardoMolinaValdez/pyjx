from typing import Self

class RequestBodyBulkCreateBuilder:
    def __init__(self) -> None:
        self.__fields = {
            "issueUpdates": []
        }

    def add_issue(self, issue: dict) -> Self:
        self.__fields["issueUpdates"].append(issue)
        return self

    def build(self) -> dict:
        return self.__fields
