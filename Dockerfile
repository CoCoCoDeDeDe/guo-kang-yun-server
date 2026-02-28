# 使用官方的 Python 3.11 轻量级基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 先复制依赖文件并安装（利用 Docker 缓存机制加速后续打包）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目代码到镜像中
COPY . .

# 暴露 8000 端口
EXPOSE 8000

# 生产环境启动命令 (使用 Uvicorn 的多 worker 模式)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]