# app\main.py
from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

from app.api.v1 import users, knowledge, governance, community, warning

import asyncio
from contextlib import asynccontextmanager
from app.db.database import engine  # 确保从 database.py 导入 engine

@asynccontextmanager
async def lifespan(app: FastAPI):
  # 启动逻辑
  yield
  # 关闭逻辑
  print("正在接收退出信号，清理资源...")
  try:
    # 使用 asyncio.wait_for 强制给关闭连接池设置 2 秒超时
    # 防止 dispose 动作本身卡死
    await asyncio.wait_for(engine.dispose(), timeout=2.0)
    print("数据库连接池已安全释放。")
  except asyncio.TimeoutError:
    print("清理超时，强制退出。")
  except Exception as e:
    print(f"清理过程中出错: {e}")

app = FastAPI(
  title=settings.PROJECT_NAME,
  lifespan=lifespan,
  docs_url="/api/docs",
  redoc_url="/api/redoc",
  openapi_url="/api/openapi.json",  
)

# ==========================================
# CORS 跨域配置
# ==========================================
# 配置允许跨域请求的前端地址
origins = [
  "http://localhost",
  "http://localhost:5173",  # Vite (Vue3/React) 默认端口
  "http://localhost",       # 👈 Capacitor Android 默认源
  "https://localhost",      # 👈 有些版本的 Capacitor 会用这个
  "capacitor://localhost",  # 👈 iOS Capacitor 常用源
  "http://localhost:3000",  # Create React App / Nuxt 默认端口
  "http://localhost:8080",  # Vue CLI 默认端口
  "http://127.0.0.1:5173",
  # "*", # ⚠️ 警告：在开发初期图省事可以写 "*" 允许所有域名，但生产环境强烈建议写死具体域名！
]

# 配置 CORS，允许 Vue 前端访问
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,            # 允许的来源列表
  allow_credentials=True,           # 允许前端携带 Cookie/凭证（如果设为True，allow_origins不能是["*"]）
  allow_methods=["*"],              # 允许所有 HTTP 方法 (GET, POST, PUT, DELETE, OPTIONS 等)
  allow_headers=["*"],              # 允许所有请求头 (Content-Type, Authorization 等)
  expose_headers=["*"],             # 允许前端访问的响应头
)

@app.get("/")
async def root():
  return {"message": "Welcome to Guo Kang Yun API"}

# 浏览器打开任何网页时，会自动向服务器请求一个名为`favicon.ico`的文件作为网页图标。
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
  # 返回“无内容”状态码
  return Response(status_code=204)

@app.get("/api/test-db", tags=["测试"])
async def test_db_connection(db: AsyncSession = Depends(get_db)):
  """
  测试数据库连接的 API
  """
  try:
    # 执行一个最简单的查询来测试连接
    result = await db.execute(text("SELECT 1"))
    value = result.scalar()
    
    if value == 1:
      return {
        "status": "success", 
        "message": "数据库连接成功！", 
        "database_url": settings.DATABASE_URL.split("@")[-1] # 只显示脱敏的URL(隐藏账号密码)
      }
  except Exception as e:
    # 如果连接失败，返回错误信息
    return {
      "status": "error", 
      "message": f"数据库连接失败: {str(e)}"
    }

# 注册模块路由
app.include_router(users.router, prefix="/api/v1/users", tags=["用户管理"])

app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["病虫害知识库"])

app.include_router(governance.router, prefix="/api/v1/governance", tags=["治理记录管理"])

app.include_router(community.router, prefix="/api/v1/community", tags=["社区与论坛(审核)"])

app.include_router(warning.router, prefix="/api/v1/warning", tags=["预警通知系统"])
