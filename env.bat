cls
del dist\pyjx-2.0.0.dev0-py3-none-any.whl
pip uninstall pyjx -y
poetry build
pip install dist\pyjx-2.0.0.dev0-py3-none-any.whl
pyjx2 run env
pyjx2 run env --path ./json_env_1.json
pyjx2 run env --path ./json_env_2.json
pyjx2 run env --path ./json_env_3.json
pyjx2 run env --path ./json_env_4.json
pyjx2 run env --path ./json_env_5_invalid.json
pyjx2 run env --path ./json_env_5_invalid_does_not_exist.json
pyjx2 config auth angelgerardomolinavaldez molineitor
pyjx2 config auth angelgerardomolinavaldez2 molineitor2
@REM pyjx2 run env --path C:\GIT\GITHUB\python\pyjx\src\pyjx\run.py
@REM pyjx2 run up
@REM pyjx2 config
@REM pyjx2 init
@REM pyjx2 run env
