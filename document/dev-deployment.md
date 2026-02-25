<!-- document\dev-deployment.md -->

# Start
## Python
### 创建并激活虚拟环境
```
# 创建虚拟环境
python -m venv venv

# 激活环境 (Windows)
.\venv\Scripts\activate
# 如果是 macOS/Linux: source venv/bin/activate
```
- **如果`python -m venv venv`失败**
  - 删除失败文件夹`rm -rf venv`或`rmdir -Recurse venv`（PowerShell）
  - 不带pip地创建`python -m venv venv --without-pip`
  - 激活并手动安装**pip**
```
.\venv\Scripts\activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
### 安装核心依赖
- **直接安装**
| 为了避免污染全局，进入`venv`虚拟环境后再安装依赖
```
pip install fastapi uvicorn[standard] sqlalchemy asyncpg alembic python-dotenv httpx pydantic-settings
```
| **删除已安装的pip**：`Remove-Item -Recurse -Force venv`
| **查看 python 环境**：在激活状态下`where.exe python`
| **查看已安装的 pip 依赖**：`pip list`
| **退出虚拟环境**：`deactivate`
| **逐个删除依赖**：`pip uninstall <包名>`（不要删除 Python 基础工具）
- **依赖 requirement.txt安装**
1. 根目录下创建`requirement.txt`文件
```
# Web 框架
fastapi>=0.115.0
uvicorn[standard]

# 数据库
sqlalchemy>=2.0.0
asyncpg
alembic

# 工具
python-dotenv
pydantic-settings
httpx
python-multipart
```
2. 在激活的虚拟环境下运行
  - `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
  - 或者`pip install -r requirements.txt`
## PostgreSQL
  对于电脑中已有一个 PostgreSQL 及在使用的项目的情况下，使用同一实例，不同数据库和端口。
**terminal commands approach**
```
CREATE DATABASE guo_kang_yuan_db;
CREATE USER fruit_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE guo_kang_yuan_db TO guo_kang_yuan_admin;
```
## 文件目录结构
guo-kang-yun-server/
├── app/
│   ├── api/            # 路由层 (v1, v2...)
│   ├── core/           # 核心配置 (config, security)
│   ├── db/             # 数据库连接与 Session 管理
│   ├── models/         # SQLAlchemy 模型 (数据库表)
│   ├── schemas/        # Pydantic 模型 (数据验证)
│   ├── services/       # 业务逻辑层
│   └── main.py         # 入口文件
├── migrations/         # Alembic 迁移脚本
├── .env                # 环境变量
├── .gitignore
├── alembic.ini
└── requirements.txt

## Git
### create a new repository on the command line
echo "# guo-kang-yun-server" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:CoCoCoDeDeDe/guo-kang-yun-server.git
git push -u origin main
### push an existing repository from the command line
git remote add origin git@github.com:CoCoCoDeDeDe/guo-kang-yun-server.git
git branch -M main
git push -u origin main