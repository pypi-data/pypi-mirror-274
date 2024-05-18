Title create CTG_Meter.exe executable

:: builds the CTG_METER python program
set "PGM=%userprofile%\PyVenv\CTG_exe\CTG_METER.py"
echo from CTG_Utils.CTG_GUI import AppMain > %PGM%
echo app_main = AppMain() >> %PGM%
echo app_main.mainloop() >> %PGM%

:: install packages

pip install CTG_Utils
pip install auto-py-to-exe

:: remote the directories buib and dist
:: set the directories buid and dist used when making the executable

set "BUILD=%userprofile%\PyVenv\CTG_exe\build"
set "DIST=%userprofile%\PyVenv\CTG_exe\dist"
rmdir /s /q %BUILD%
rmdir /s /q %DIST%

:: set the default directories
:: ICON contains the icon file with the format.ico
:: PGM contain the application lauch python program

set "ICON=%userprofile%/PyVenv/CTG_exe/venv/Lib/site-packages/CTG_Utils/CTG_Func/CTG_RefFiles/logoctg4.ico"
set "DATA=%userprofile%/PyVenv/CTG_exe/venv/Lib/site-packages/CTG_Utils;CTG_Utils/"

:: make the executable 
pyinstaller --noconfirm --onefile --console^
 --icon "%ICON%"^
 --add-data "%DATA%"^
 "%PGM%"