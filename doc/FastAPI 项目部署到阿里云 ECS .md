# FastAPI 项目部署到阿里云 ECS 完整记录

## 一、部署准备

### 1.1 你需要有的东西

| 项目 | 说明 |
|------|------|
| 阿里云 ECS 服务器 | 操作系统：Ubuntu 22.04，公网 IP：112.124.26.125 |
| Docker 镜像 | 你的 FastAPI 项目打包成的镜像 |
| （可选）域名 | 如 zhuor.xyz，用于域名访问 |

### 1.2 架构图

```text
用户浏览器
    ↓
http://112.124.26.125:8080/docs
    ↓
阿里云服务器 (112.124.26.125)
    ↓
阿里云安全组（入方向规则：放行 8080 端口）
    ↓
Docker Nginx 容器 (监听端口 8080，反向代理到 127.0.0.1:8001)
    ↓
Docker FastAPI 容器 (映射端口：-p 8001:8000)
    ↓
FastAPI 应用 (容器内监听 8000 端口)
    ↓
返回响应
```

## 二、部署步骤

### 第一步：在阿里云 ECS 上安装 Docker

```bash
# 更新系统包
sudo apt update

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### 第二步：构建或拉取镜像

```bash
# 方式1：在服务器上构建（从源代码）
docker build -t my-agent:latest .

# 方式2：从阿里云容器镜像仓库拉取
docker login crpi-ckze2swpfquw5fy5.cn-hangzhou.personal.cr.aliyuncs.com
docker pull crpi-ckze2swpfquw5fy5.cn-hangzhou.personal.cr.aliyuncs.com/ericagent/my-agent:latest
docker tag crpi-ckze2swpfquw5fy5.cn-hangzhou.personal.cr.aliyuncs.com/ericagent/my-agent:latest my-agent:latest
```

### 第三步：运行容器

```bash
docker run -d \
  --name my-agent \
  --restart=always \
  -p 8001:8000 \
  my-agent:latest
```

| 参数 | 含义 |
|------|------|
| `-d` | 后台运行 |
| `--name my-agent` | 容器名称 |
| `--restart=always` | 服务器重启后自动启动容器 |
| `-p 8001:8000` | 宿主机 8001 端口映射到容器 8000 端口 |
| `my-agent:latest` | 使用的镜像名 |

### 第四步：运行 Nginx 容器

创建 Nginx 配置文件 `~/nginx/conf.d/default.conf`：

```bash
mkdir -p ~/nginx/conf.d

tee ~/nginx/conf.d/default.conf > /dev/null << 'EOF'
server {
    listen 8080;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

运行 Nginx 容器：

```bash
docker run -d \
  --name nginx \
  --restart=always \
  -p 8001:8000 \
  -v ~/nginx/conf.d:/etc/nginx/conf.d \
  nginx:latest
```

| 配置项 | 含义 |
|--------|------|
| `listen 8080` | Nginx 监听 8080 端口 |
| `server_name _` | 匹配所有请求，不限定域名 |
| `proxy_pass http://127.0.0.1:8001` | 反向代理到 FastAPI 容器映射的端口 |
| `-v ~/nginx/conf.d:/etc/nginx/conf.d` | 挂载配置文件到容器内 |

### 第五步：配置阿里云安全组（入方向规则）

登录阿里云控制台 → ECS 实例 → 安全组 → 配置规则

添加入方向规则：

| 参数 | 值 | 说明 |
|------|-----|------|
| 规则方向 | 入方向 | 外部访问服务器 |
| 授权策略 | 允许 | 放行 |
| 协议类型 | TCP | 传输协议 |
| 端口范围 | 8080/8080 | 你暴露的端口 |
| 授权对象 | 0.0.0.0/0 | 允许所有 IP 访问 |
| 优先级 | 1 | 最高优先级 |

> **核心概念：** 入方向 = 外部流量进入服务器。出方向 = 服务器内部访问外部。

### 第六步：测试访问

```bash
# 在本地电脑访问
http://112.124.26.125:8080/docs
```

如果能打开 Swagger 文档，说明部署成功 🎉

## 三、域名备案

### 3.1 哪些情况需要备案

| 访问方式 | 需要备案？ | 原因 |
|----------|-----------|------|
| `http://112.124.26.125:8080/docs` | ❌ 不需要 | 直接用 IP，不涉及域名 |
| `http://zhuor.xyz:8080/docs` | ✅ 必须备案 | 域名解析到大陆服务器，无论什么端口都会被拦截 |
| `http://zhuor.xyz`（默认 80 端口） | ✅ 必须备案 | 域名 + 80 端口 |
| `https://zhuor.xyz`（默认 443 端口） | ✅ 必须备案 | 域名 + 443 端口 |

> **核心结论：** 只要域名解析到大陆服务器 IP，阿里云就会拦截，与端口无关。唯一不需要备案的方式是用 IP 直接访问。

### 3.2 阿里云的拦截机制

阿里云不是单纯看端口，而是检测 HTTP 请求头中的 `Host` 字段。当 `Host` 包含未备案域名时，直接在网络层拦截，请求根本到不了你的服务器。

```text
用户访问 http://zhuor.xyz:8080/docs
    ↓
请求到达阿里云网络边界
    ↓
阿里云检测到 Host: zhuor.xyz
    ↓
查询备案系统 → 未备案
    ↓
直接返回拦截页面 ❌（请求根本没到你的 Nginx）
```

### 3.3 为什么 IP 访问可以

| 访问方式 | 是否带域名 | 结果 |
|----------|-----------|------|
| `http://112.124.26.125:8080/docs` | ❌ 不带域名（直接用 IP） | ✅ 正常访问 |
| `http://zhuor.xyz:8080/docs` | ✅ 带域名 `Host: zhuor.xyz` | ❌ 被拦截 |

阿里云通过检测 HTTP 请求头中的 `Host` 字段来判断是否使用了域名，跟端口号无关。

## 四、最终结论

### 推荐的访问方式

**测试接口阶段：**

```text
http://112.124.26.125:8080/docs
```

- ✅ 不需要域名
- ✅ 不需要备案
- ✅ Nginx 反向代理，架构更清晰
- ✅ 简单直接

**正式上线阶段（如果需要）：**

1. 注册可备案域名（如 `.com`、`.cn`、`.xyz`）
2. 完成 ICP 备案
3. Nginx 改回监听 80/443 端口，配置入方向规则 和 SSL 证书
4. 使用 `https://yourdomain.com` 访问