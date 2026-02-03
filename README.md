# 启动前端服务
## 1、进入目录
cd frontend 
## 2、启动
npm run dev 

# 启动后端服务
## 1、进入目录
cd backend 
## 2、启动
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}