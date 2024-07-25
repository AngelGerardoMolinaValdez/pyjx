import os
import json

class GlobalConfig:
    __config: dict = None

    @classmethod
    def read_config(cls):
        if cls.__config is not None:
            return cls.__config

        user_home_path = os.path.expanduser("~")
        pyjx_config_path = os.path.join(user_home_path, ".pyjx", "general.json")

        if not os.path.exists(pyjx_config_path):
            return

        with open(pyjx_config_path, "w", encoding="utf-8") as pyjx_config:
            try:
                config: dict = json.load(pyjx_config)
            except json.JSONDecodeError:
                raise ValueError("El json de configuración global contiene errores y no es posible obtener la información de autenticación.")

        return config

    @classmethod
    def get_auth(cls):
        if cls.__config is not None:
            return cls.__config.get("auth")
