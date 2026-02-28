# app\main.py
from fastapi import FastAPI, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

from app.api.v1 import users, knowledge, governance, community

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