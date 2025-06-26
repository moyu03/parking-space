@echo off
setlocal

REM === 设置您的 Anaconda 路径 ===
set ANACONDA_PATH=D:\anaconda

REM === 设置项目路径 ===
set PROJECT_PATH=%~dp0

REM === 清理旧构建 ===
rd /s /q build 2>nul
del /q ParkingSystem.spec 2>nul

REM === 使用正确的 Python 环境 ===
call "%ANACONDA_PATH%\Scripts\activate.bat"

REM === 执行打包命令 ===
pyinstaller --onefile --noconsole ^
--name ParkingSystem ^
--icon "%PROJECT_PATH%icon.ico" ^
--add-data "%PROJECT_PATH%core;core" ^
--add-data "%PROJECT_PATH%ui;ui" ^
--add-data "%PROJECT_PATH%models;models" ^
--add-data "%PROJECT_PATH%utils;utils" ^
--add-binary "%ANACONDA_PATH%\python312.dll;." ^
--add-binary "%ANACONDA_PATH%\DLLs\*.dll;DLLs" ^
--collect-all tkinter ^
--collect-all pywin32 ^
--collect-all sqlite3 ^
--hidden-import _ctypes ^
--hidden-import encodings.utf_8 ^
--hidden-import encodings.mbcs ^
--hidden-import unicodedata ^
--runtime-tmpdir . ^
--paths "%ANACONDA_PATH%" ^
--upx-disable ^
--workpath build ^
--specpath build ^
--distpath dist ^
"%PROJECT_PATH%main.py"

REM === 验证打包结果 ===
if exist "dist\ParkingSystem.exe" (
    echo 打包成功！文件位于: dist\ParkingSystem.exe
    
    REM 复制依赖文件到 dist 目录
    copy "%ANACONDA_PATH%\python312.dll" "dist\python312.dll" >nul
    echo 已复制 python312.dll 到输出目录
    
    mkdir "dist\DLLs" 2>nul
    copy "%ANACONDA_PATH%\DLLs\*.dll" "dist\DLLs\" >nul
    echo 已复制所有依赖 DLL 到 dist\DLLs 目录
) else (
    echo 打包失败，请检查错误信息！
)

endlocal
pause