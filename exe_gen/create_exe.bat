@REM pyinstaller --onefile pyemmo/api/pyleecan/__main__.py
pyinstaller --onefile --name pyemmo --icon pyemmo.ico ^
-p C:\Users\ganser\AppData\Local\Programs\swat-em ^
--collect-data pyemmo.script ^
--collect-data pyemmo.script.material ^
--collect-submodules pyleecan.Classes ^
--specpath exe_gen ^
workingDirectory\pyleecan_api_interactive.py

@REM --hidden-import pyleecan.Classes.Unit --hidden-import pyleecan.Classes.ModelBH
