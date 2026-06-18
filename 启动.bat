@echo off
chcp 65001 >nul
title 幼师助手 - 启动中...

echo.
echo   🦞 幼师助手 — 正在启动...
echo   ────────────────────────────
echo.

:: 检查 Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ 未检测到 Python，请先安装 Python 3
    echo   📥 下载地址: https://www.python.org/downloads/
    echo   安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

:: 检查/安装 Flask
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo   📦 正在安装依赖（首次运行需要几秒）...
    pip install flask -q
    if %errorlevel% neq 0 (
        echo   ❌ 安装失败，请检查网络连接
        pause
        exit /b 1
    )
)

:: 创建数据目录
if not exist "data\records" mkdir "data\records"

echo   ✅ 服务启动成功！
echo   ────────────────────────────
echo   🌐 浏览器即将打开: http://localhost:5000
echo   📁 数据保存在: data\records\
echo   ⚠️  关闭此窗口将停止服务
echo.

:: 启动浏览器
start "" http://localhost:5000

:: 启动服务
python server.py

pause
