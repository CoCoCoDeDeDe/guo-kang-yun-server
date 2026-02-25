# app\main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
  title=settings.PROJECT_NAME,
  docs_url="/api/docs",
  redoc_url="/api/redoc",
  openapi_url="/api/openapi.json",  
)

# 配置 CORS，允许 Vue 前端访问
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # 开发阶段允许所有，生产环境需限制
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
async def root():
  return {"message": "Welcome to Guo Kang Yun API"}