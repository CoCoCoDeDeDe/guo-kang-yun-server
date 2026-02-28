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
  
  # === 新增邮件发送 SMTP 配置 ===
  MAIL_USERNAME: str = "你的QQ号@qq.com"          # 你的发件邮箱
  MAIL_PASSWORD: str = "你的邮箱授权码"           # 填入刚刚获取的授权码 (不是登录密码!)
  MAIL_FROM: str = "你的QQ号@qq.com"              # 发件人邮箱 (通常同上)
  MAIL_PORT: int = 465                            # QQ / 163 邮箱的 SSL 端口通常是 465
  MAIL_SERVER: str = "smtp.qq.com"                # 163邮箱请填 smtp.163.com
  MAIL_FROM_NAME: str = "果康云预警中心"           # 邮件发件人昵称
  MAIL_STARTTLS: bool = False                     # 端口465对应SSL，此处设为False
  MAIL_SSL_TLS: bool = True                       # 端口465设为True
  USE_CREDENTIALS: bool = True
  VALIDATE_CERTS: bool = True
  
  model_config = SettingsConfigDict(env_file=".env")
  
# 实例化，这样别的文件才可以 import settings
settings = Settings()
