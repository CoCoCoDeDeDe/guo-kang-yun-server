# app\models\__init__.py
# 导入基础类，方便在 Alembic 的 env.py 中直接引入 target_metadata = Base.metadata
from app.db.database import Base

# 导入所有模型，确保它们被注册到 SQLAlchemy 的元数据(metadata)中
from app.models.user import User, VerificationCode
from app.models.knowledge import PestInfo, PreventionScheme
from app.models.governance import GovernanceRecord
from app.models.community import Article, Post, AuditLog
from app.models.warning import WarningMessage

# 可选：控制包导出的内容
__all__ = [
  "Base",
  "User",
  "VerificationCode",
  "PestInfo",
  "PreventionScheme",
  "GovernanceRecord",
  "Article",
  "Post",
  "AuditLog",
  "WarningMessage"
]