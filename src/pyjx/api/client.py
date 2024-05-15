from typing import ClassVar
from json import JSONDecodeError
from requests import get, post, put, delete, Response
from requests.auth import AuthBase
from errors import ClientError, ServerError


class Client:
    __url: ClassVar = None
    __auth: ClassVar = None
    __request_details: ClassVar = {
        "verify": True,
        "timeout": 10
    }

    @classmethod
    def configure(cls, url: str, auth: AuthBase, verify: bool = True, timeout: int = 10):
        cls.__url = url
        cls.__auth = auth
        cls.__request_details = {
            "verify": verify,
            "timeout": timeout
        }

    @classmethod
    def post(cls, path, **data):
        response = post(
            cls.__url + path,
            auth=cls.__auth,
            **data,
            **cls.__request_details
        )

        cls.raise_for_status_code_error(response)

        try:
            json = response.json()
        except JSONDecodeError:
            json = {}

        return json

    @classmethod
    def get(cls, path, **data):
        response = get(
            cls.__url + path,
            auth=cls.__auth,
            **data,
            **cls.__request_details
        )

        cls.raise_for_status_code_error(response)

        return response.json()

    @classmethod
    def delete(cls, path):
        response = delete(
            cls.__url + path,
            auth=cls.__auth,
            **cls.__request_details
        )

        cls.raise_for_status_code_error(response)

        try:
            json = response.json()
        except JSONDecodeError:
            json = {}

        return json

    @classmethod
    def put(cls, path, **data):
        response = put(
            cls.__url + path,
            auth=cls.__auth,
            **data,
            **cls.__request_details
        )

        cls.raise_for_status_code_error(response)

        try:
            json = response.json()
        except JSONDecodeError:
            json = {}

        return json

    @staticmethod
    def raise_for_status_code_error(response: Response) -> None:
        if response.status_code >= 400 and response.status_code < 500:
            raise ClientError(response)

        if response.status_code >= 500:
            raise ServerError(response)
