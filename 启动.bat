@echo off
chcp 65001 >nul
title 幼师助手

echo.
echo   🦞 幼师助手 — 启动中...
echo   ────────────────────────────

:: 切到脚本所在目录
cd /d "%~dp0"

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo   ❌ 没有检测到 Python，请先安装 Python 3
    echo   📥 https://www.python.org/downloads/
    echo   ⚠️ 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo   ✅ Python 检测成功

:: 安装 Flask（显示进度）
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo   📦 首次运行，正在安装依赖...
    python -m pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo.
        echo   ❌ 自动安装失败，请手动执行：
        echo      pip install flask
        echo   如果仍失败，试试：
        echo      python -m pip install flask --user
        echo.
        pause
        exit /b 1
    )
)

:: 创建数据目录
if not exist "data\records" mkdir "data\records"

cls
echo.
echo   🦞 幼师助手
echo   ────────────────────────────
echo   ✅ 服务已启动
echo   🌐 浏览器即将打开: http://localhost:5000
echo   📁 数据存储在: data\records\
echo.
echo   ⚠️  关闭此窗口 = 停止服务
echo   ────────────────────────────
echo.

:: 先开浏览器（等 1 秒让服务先起来）
start "" http://localhost:5000

:: 启动 Flask
python server.py

pause
