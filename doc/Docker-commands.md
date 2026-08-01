# Docker 命令使用指南

## 基础信息

```bash
# 查看 Docker 版本
docker --version

# 查看 Docker 信息
docker info

# 查看 Docker 状态
docker system df
```

## 镜像操作

```bash
# 构建镜像
docker build -t my-fastapi-app .

# 带缓存构建镜像
docker build -t my-fastapi-app . --no-cache

# 查看镜像列表
docker images

# 查看镜像历史
docker history my-fastapi-app

# 拉取镜像
docker pull python:3.14

# 推送镜像到仓库
docker push my-fastapi-app:latest

# 删除镜像
docker rmi my-fastapi-app

# 强制删除镜像
docker rmi -f my-fastapi-app

# 删除所有未使用的镜像
docker image prune -a

# 清理构建缓存
docker builder prune
```

## 容器操作

```bash
# 运行容器
docker run -d -p 8000:8000 --name my-fastapi-container my-fastapi-app

# 交互式运行容器 (进入容器)
docker run -it --name my-container my-fastapi-app /bin/bash

# 运行容器并挂载目录
docker run -d -p 8000:8000 -v /host/path:/container/path my-fastapi-app

# 运行容器并设置环境变量
docker run -d -p 8000:8000 -e DATABASE_URL=xxx my-fastapi-app

# 运行容器并设置网络
docker run -d --network host my-fastapi-app

# 查看运行中的容器
docker ps

# 查看所有容器 (包括已停止)
docker ps -a

# 查看容器详细信息
docker inspect my-fastapi-container

# 查看容器实时资源使用
docker stats

# 查看容器进程
docker top my-fastapi-container

# 进入运行中的容器
docker exec -it my-fastapi-container /bin/bash

# 复制文件到容器
docker cp file.txt my-fastapi-container:/app/

# 从容器复制文件出来
docker cp my-fastapi-container:/app/file.txt ./

# 查看容器日志
docker logs my-fastapi-container

# 实时查看容器日志
docker logs -f my-fastapi-container

# 查看最近 100 行日志
docker logs --tail 100 my-fastapi-container
```

## 容器生命周期

```bash
# 启动容器
docker start my-fastapi-container

# 停止容器
docker stop my-fastapi-container

# 重启容器
docker restart my-fastapi-container

# 暂停容器
docker pause my-fastapi-container

# 取消暂停容器
docker unpause my-fastapi-container

# 终止容器
docker kill my-fastapi-container

# 删除已停止的容器
docker rm my-fastapi-container

# 强制删除运行中的容器
docker rm -f my-fastapi-container

# 删除所有已停止的容器
docker container prune

# 查看容器更改
docker diff my-fastapi-container
```

## 网络操作

```bash
# 查看网络列表
docker network ls

# 创建网络
docker network create my-network

# 查看网络详情
docker network inspect my-network

# 删除网络
docker network rm my-network

# 将容器连接到网络
docker network connect my-network my-container

# 从网络断开容器
docker network disconnect my-network my-container
```

## 卷操作

```bash
# 查看卷列表
docker volume ls

# 创建卷
docker volume create my-volume

# 查看卷详情
docker volume inspect my-volume

# 删除未使用的卷
docker volume prune

# 删除指定卷
docker volume rm my-volume
```

## Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 后台启动并构建
docker-compose up -d --build

# 停止所有服务
docker-compose down

# 停止并删除卷
docker-compose down -v

# 查看服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f web

# 查看服务状态
docker-compose ps

# 执行服务命令
docker-compose exec web python manage.py

# 重启单个服务
docker-compose restart web

# 构建镜像 (不使用缓存)
docker-compose build --no-cache

# 拉取服务依赖的镜像
docker-compose pull

# 扩展服务 (运行多个实例)
docker-compose up -d --scale web=3
```

## 清理命令

```bash
# 清理未使用的容器
docker container prune -f

# 清理未使用的镜像
docker image prune -a -f

# 清理未使用的卷
docker volume prune -f

# 清理未使用的网络
docker network prune -f

# 清理构建缓存
docker builder prune -f

# 清理所有未使用资源 (容器、镜像、卷、网络)
docker system prune -a -f

# 清理数据 (包括卷)
docker system prune -a -f --volumes
```

## 常用参数

| 参数 | 说明 |
|------|------|
| `-d` | 后台运行容器 |
| `-p` | 端口映射 (主机端口:容器端口) |
| `--name` | 指定容器名称 |
| `-v` | 挂载卷 |
| `-e` | 设置环境变量 |
| `-it` | 交互式运行 (TTY + stdin) |
| `--rm` | 容器退出后自动删除 |
| `--network` | 指定网络 |
| `-m` | 限制内存 |
| `--cpus` | 限制 CPU 核心数 |
| `--restart` | 重启策略 (always/on-failure/unless-stopped) |
| `-w` | 设置工作目录 |
| `--privileged` | 授予特权 |
| `--link` | 链接到其他容器 (已废弃) |