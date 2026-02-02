安装依赖：pip install -r requirements.txt

加载环境变量：source ./setenv.sh

#环境变量 PORT 存在，用 $PORT；环境变量 PORT 不存在，用 8000
启动服务：uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}