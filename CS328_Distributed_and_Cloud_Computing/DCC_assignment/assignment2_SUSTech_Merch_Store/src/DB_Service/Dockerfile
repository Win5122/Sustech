# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的 requirements.txt 文件复制到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器
COPY . /app

# 暴露数据库服务端口
EXPOSE 5432

# 启动数据库服务
CMD ["python", "DB_Client.py"]
