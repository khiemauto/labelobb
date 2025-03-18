@echo off

REM Build file .exe bằng PyInstaller
pyinstaller .\labelImg.spec
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PyInstaller build failed!
    exit /b %ERRORLEVEL%
)

REM Sao chép thư mục data vào dist
xcopy "data" "dist\data" /E /I
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to copy 'data' folder!
    exit /b %ERRORLEVEL%
)

echo Build and copy completed successfully!