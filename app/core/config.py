# app\core\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  # 此处变量名必须和 .env 中的 KEY 一致（不区分大小写）
  DATABASE_URL: str = "postgresql+asyncpg://guo_kang_yuan_admin:guokangyun@localhost:5432/guo_kang_yuan_db"
  PROJECT_NAME: str = "果康云"
  
  model_config = SettingsConfigDict(env_file=".env")
  
# 实例化，这样别的文件才可以 import settings
settings = Settings()