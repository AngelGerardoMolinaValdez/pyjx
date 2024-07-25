import os
import json

class SetAuthCommand:
    def __init__(self, username, password) -> None:
        self.__usr = username
        self.__pwd = password

    def execute(self):
        user_home_path = os.path.expanduser("~")
        pyjx_config_path = os.path.join(user_home_path, ".pyjx", "general.json")

        data = {
            "auth": {
                "username": self.__usr,
                "password": self.__pwd
            }
        }

        if not os.path.exists(pyjx_config_path):
            os.makedirs(os.path.dirname(pyjx_config_path))
            with open(pyjx_config_path, "w", encoding="utf-8") as pyjx_config:
                json.dump(data, pyjx_config)

        else:
            with open(pyjx_config_path, "r", encoding="utf-8") as pyjx_config:
                try:
                    content: dict = json.load(pyjx_config)
                    content.update(data)
                except json.JSONDecodeError:
                    content = data
            
            with open(pyjx_config_path, "w", encoding="utf-8") as pyjx_config:
                json.dump(content, pyjx_config, indent=4)
