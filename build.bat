@echo off
echo ======================================
echo Todo List 应用打包工具
echo ======================================
echo.

echo [1/3] 检查并安装依赖...
pip install -r requirements.txt
echo.

echo [2/3] 清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "todolist.spec" del /q todolist.spec
echo.

echo [3/3] 开始打包应用...
pyinstaller --name="TodoList" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data="README.md;." ^
    --noconsole ^
    --clean ^
    todolist.py

echo.
if exist "dist\TodoList.exe" (
    echo ======================================
    echo 打包完成！
    echo 可执行文件位置: dist\TodoList.exe
    echo ======================================
) else (
    echo ======================================
    echo 打包失败，请检查错误信息
    echo ======================================
)
echo.
pause
