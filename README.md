# 启动前端服务
cd frontend 
npm run dev 

# 启动后端服务
cd backend 
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}