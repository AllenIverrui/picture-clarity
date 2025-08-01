
@echo off
chcp 65001 >nul
echo 🚀 图片高清化工具启动中...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.7+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Node.js，请先安装Node.js 16+
    echo 下载地址：https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js已安装
echo.

REM 安装后端依赖
echo 📦 正在安装后端依赖包...
cd backend

REM 先尝试最小化依赖
pip install -r requirements-minimal.txt
if errorlevel 1 (
    echo ❌ 最小化依赖安装失败，尝试逐个安装...
    pip install sanic==23.6.0
    pip install pillow==10.0.1
    pip install python-multipart==0.0.6
    pip install aiofiles==23.2.1
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
)
cd ..

echo ✅ 后端依赖安装完成
echo.

REM 安装前端依赖
echo 📦 正在安装前端依赖包...
cd frontend
npm install
if errorlevel 1 (
    echo ❌ 前端依赖安装失败，请检查网络连接
    pause
    exit /b 1
)
cd ..

echo ✅ 前端依赖安装完成
echo.

REM 启动后端服务
echo 🌐 正在启动后端服务...
start "后端服务" cmd /k "cd backend && python app-basic.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 启动前端服务
echo 🌐 正在启动前端服务...
start "前端服务" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ 服务启动完成！
echo 📱 前端地址：http://localhost:3000
echo 🔧 后端地址：http://localhost:8000
echo.
echo 按任意键退出...
pause >nul 