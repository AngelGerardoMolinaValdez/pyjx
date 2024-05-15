from requests import HTTPError, get

class ClientError(HTTPError):
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.reason = response.reason
        self.message = f"Client Error: {self.reason}. Status {self.status_code}. Message: {response.text}. For more information visit https://developer.mozilla.org/es/docs/Web/HTTP/Status/{self.status_code}"
        super().__init__(self.message)

    def __str__(self):
        return self.message

class ServerError(HTTPError):
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        self.reason = response.reason
        self.message = f"Server Error: {self.reason}. Status {self.status_code}. Message: {response.text}. For more information visit https://developer.mozilla.org/es/docs/Web/HTTP/Status/{self.status_code}"
        super().__init__(self.message)
    
    def __str__(self):
        return self.message
