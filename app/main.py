# app\main.py
from fastapi import FastAPI, Response
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

# 浏览器打开任何网页时，会自动向服务器请求一个名为`favicon.ico`的文件作为网页图标。
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  # 返回“无内容”状态码
  return Response(status_code=204)