# app\core\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  # 此处变量名必须和 .env 中的 KEY 一致（不区分大小写）
  DATABASE_URL: str = "postgresql+asyncpg://guo_kang_yun_admin:guokangyun@localhost:5432/guo_kang_yun_db"
  PROJECT_NAME: str = "果康云"
  
  # === JWT 变量 ===
  # 生产环境中，SECRET_KEY 应该放在 .env 文件里。这里先写死用于开发。
  # 可以用命令 `openssl rand -hex 32` 生成一个随机字符串替换下面的值
  SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # Token 有效期设为 7 天
  
  model_config = SettingsConfigDict(env_file=".env")
  
# 实例化，这样别的文件才可以 import settings
settings = Settings()