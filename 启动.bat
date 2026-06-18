@echo off
chcp 65001 >nul
title 幼师助手

cd /d "%~dp0"

echo.
echo   🦞 幼师助手 — 启动中...
echo   ────────────────────────────

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ 没有检测到 Python 3
    echo   📥 https://www.python.org/downloads/
    echo   ⚠️ 安装时务必勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo   ✅ Python 已就绪
echo   📁 数据文件夹: data\records\
if not exist "data\records" mkdir "data\records"

echo   🌐 打开浏览器: http://localhost:5000
echo.
echo   ⚠️  关闭此窗口 = 停止服务
echo   ────────────────────────────

start "" http://localhost:5000
python server.py
pause
