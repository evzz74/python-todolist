@echo off
echo ======================================
echo Todo List Build Tool
echo ======================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
echo.

echo [2/3] Cleaning old build files...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "todolist.spec" del /q todolist.spec
echo.

echo [3/3] Building application...
pyinstaller --name="TodoList" --onefile --windowed --noconsole --clean todolist.py

echo.
if exist "dist\TodoList.exe" (
    echo ======================================
    echo Build successful!
    echo Output: dist\TodoList.exe
    echo ======================================
) else (
    echo ======================================
    echo Build failed, please check errors
    echo ======================================
)
echo.
pause
