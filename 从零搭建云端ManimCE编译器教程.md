# 从零开始搭建云端ManimCE编译器完整教程

## 目录
1. [前言](#前言)
2. [方案概述](#方案概述)
3. [方案一：使用Binder的云端解决方案（推荐新手）](#方案一使用binder的云端解决方案推荐新手)
4. [方案二：本地Docker环境搭建](#方案二本地docker环境搭建)
5. [方案三：本地Python环境搭建](#方案三本地python环境搭建)
6. [方案四：自建云端服务器部署](#方案四自建云端服务器部署)
7. [常见问题解决](#常见问题解决)
8. [进阶使用技巧](#进阶使用技巧)

---

## 前言

ManimCE（Manim Community Edition）是一个强大的数学动画制作库，但安装配置对新手来说较为复杂。本教程将教您如何搭建一个云端编译环境，让您可以在浏览器中直接编写和运行Manim动画，无需复杂的本地配置。

### 什么是ManimCE？
- 一个用Python编写数学动画的库
- 可以制作高质量的教学动画
- 支持LaTeX数学公式渲染
- 广泛用于数学教育视频制作

### 为什么需要云端编译器？
- 避免复杂的本地环境配置
- 跨平台使用，只需浏览器
- 快速体验和学习
- 团队协作更方便

---

## 方案概述

我们提供四种搭建方案，按难度递增：

| 方案 | 难度 | 适用场景 | 优点 | 缺点 |
|------|------|----------|------|------|
| Binder云端 | ⭐ | 快速体验 | 零配置，即开即用 | 临时环境，无法持久保存 |
| Docker本地 | ⭐⭐ | 稳定开发 | 环境一致，易部署 | 需要安装Docker |
| Python本地 | ⭐⭐⭐ | 长期开发 | 自由度高，性能好 | 配置复杂 |
| 自建服务器 | ⭐⭐⭐⭐ | 团队使用 | 完全控制，可定制 | 需要服务器运维知识 |

---

## 方案一：使用Binder的云端解决方案（推荐新手）

### 1.1 什么是Binder？
Binder是一个免费的云端Jupyter服务，可以直接运行GitHub上的笔记本项目。

### 1.2 快速开始（5分钟上手）

#### 步骤1：访问现成的环境
点击这个链接直接体验：
```
https://mybinder.org/v2/gh/shiloong/Cloud-Manim-Compiler/HEAD?urlpath=/doc/tree/Cloud-Manim-Compiler-JupyterLab.ipynb
```

#### 步骤2：等待环境启动
- 首次启动需要3-5分钟
- 看到JupyterLab界面即可开始使用

#### 步骤3：运行第一个动画
在笔记本中运行以下代码：
```python
%%manim -qm FirstScene

class FirstScene(Scene):
    def construct(self):
        # 创建一个圆形
        circle = Circle(color=BLUE)
        # 显示圆形


        
        self.play(Create(circle))
        # 等待一秒
        self.wait()
```

### 1.3 创建自己的Binder项目

如果想要自定义环境，可以创建自己的GitHub仓库：

#### 步骤1：创建GitHub仓库
1. 登录GitHub，创建新仓库（如：my-manim-binder）
2. 选择Public（公开）仓库

#### 步骤2：创建配置文件
在仓库根目录创建以下文件：

**文件：`environment.yml`**
```yaml
name: manim-env
channels:
  - conda-forge
  - default
dependencies:
  - python=3.9
  - pip
  - notebook
  - jupyterlab
  - numpy
  - matplotlib
  - pip:
    - manim
    - jupyter-server-proxy
```

**文件：`postBuild`**
```bash
#!/bin/bash
# 安装中文字体
sudo apt-get update
sudo apt-get install -y fonts-wqy-zenhei fonts-wqy-microhei
```

**文件：`README.md`**
```markdown
# 我的Manim云端环境

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/你的用户名/my-manim-binder/HEAD?urlpath=lab)

点击上方按钮启动环境！
```

#### 步骤3：创建示例笔记本
创建文件：`examples.ipynb`，包含一些基础示例。

#### 步骤4：获取Binder链接
将README中的链接改为：
```
https://mybinder.org/v2/gh/你的用户名/my-manim-binder/HEAD?urlpath=lab
```

---

## 方案二：本地Docker环境搭建

### 2.1 前置要求
- 安装Docker Desktop（Windows/Mac）或Docker Engine（Linux）
- 基本的命令行操作知识

### 2.2 安装Docker

#### Windows系统：
1. 下载Docker Desktop：https://www.docker.com/products/docker-desktop/
2. 安装并重启电脑
3. 启动Docker Desktop

#### Mac系统：
```bash
# 使用Homebrew安装
brew install --cask docker
```

#### Linux系统：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### 2.3 创建Dockerfile

创建工作目录：
```bash
mkdir manim-docker
cd manim-docker
```

创建`Dockerfile`：
```dockerfile
# 基于官方ManimCE镜像
FROM manimcommunity/manim:v0.18.0

# 切换到root用户安装依赖
USER root

# 安装中文字体和其他依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装Jupyter相关包
RUN pip install --no-cache-dir \
    notebook \
    jupyterlab \
    ipywidgets \
    matplotlib \
    numpy

# 创建工作目录
RUN mkdir -p /manim/notebooks
WORKDIR /manim

# 切换回manim用户
ARG NB_USER=manimuser
USER ${NB_USER}

# 暴露Jupyter端口
EXPOSE 8888

# 启动命令
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
```

### 2.4 构建和运行

#### 构建镜像：
```bash
docker build -t my-manim-jupyter .
```

#### 运行容器：
```bash
docker run -p 8888:8888 -v ${PWD}/notebooks:/manim/notebooks my-manim-jupyter
```

#### 访问环境：
打开浏览器访问：`http://localhost:8888`

### 2.5 创建docker-compose.yml（可选）

为了方便管理，创建`docker-compose.yml`：
```yaml
version: '3.8'
services:
  manim-jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/manim/notebooks
      - ./outputs:/manim/media
    environment:
      - JUPYTER_ENABLE_LAB=yes
```

使用方法：
```bash
# 启动
docker-compose up

# 后台运行
docker-compose up -d

# 停止
docker-compose down
```

---

## 方案三：本地Python环境搭建

### 3.1 系统要求
- Python 3.8-3.11
- FFmpeg（用于视频处理）
- LaTeX（用于数学公式）

### 3.2 安装基础依赖

#### Windows系统：

**安装Python：**
1. 从 https://python.org 下载Python 3.9
2. 安装时勾选"Add to PATH"

**安装FFmpeg：**
```powershell
# 使用Chocolatey
choco install ffmpeg

# 或下载并手动配置PATH
# https://ffmpeg.org/download.html
```

**安装LaTeX：**
```powershell
# 安装MiKTeX
choco install miktex
```

#### Mac系统：
```bash
# 安装Homebrew（如果没有）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装依赖
brew install python@3.9 ffmpeg
brew install --cask mactex
```

#### Linux系统：
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip ffmpeg texlive-full

# CentOS/RHEL
sudo yum install python3 python3-pip ffmpeg texlive
```

### 3.3 创建Python环境

#### 使用venv：
```bash
# 创建虚拟环境
python -m venv manim-env

# 激活环境
# Windows:
manim-env\Scripts\activate
# Mac/Linux:
source manim-env/bin/activate
```

#### 使用conda（推荐）：
```bash
# 安装Miniconda
# 下载：https://docs.conda.io/en/latest/miniconda.html

# 创建环境
conda create -n manim-env python=3.9
conda activate manim-env
```

### 3.4 安装ManimCE和Jupyter

```bash
# 安装ManimCE
pip install manim

# 安装Jupyter
pip install jupyter jupyterlab

# 安装额外依赖
pip install matplotlib numpy scipy pillow
```

### 3.5 配置中文字体

创建字体安装脚本`install_fonts.py`：
```python
import os
import sys
import platform
import subprocess
import requests
from pathlib import Path

def install_chinese_fonts():
    """安装中文字体"""
    system = platform.system()
    
    if system == "Windows":
        font_dir = "C:\\Windows\\Fonts"
    elif system == "Darwin":  # macOS
        font_dir = "/Library/Fonts"
    elif system == "Linux":
        font_dir = os.path.expanduser("~/.local/share/fonts")
        os.makedirs(font_dir, exist_ok=True)
    
    fonts = [
        ("SimHei.ttf", "https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf"),
        ("SourceHanSans.ttc", "https://github.com/adobe-fonts/source-han-sans/raw/release/OTC/SourceHanSans.ttc")
    ]
    
    for font_name, url in fonts:
        font_path = os.path.join(font_dir, font_name)
        if not os.path.exists(font_path):
            print(f"下载字体: {font_name}")
            try:
                response = requests.get(url)
                with open(font_path, 'wb') as f:
                    f.write(response.content)
                print(f"安装成功: {font_name}")
            except Exception as e:
                print(f"安装失败: {e}")
    
    # Linux需要更新字体缓存
    if system == "Linux":
        subprocess.run(["fc-cache", "-f", "-v"])

if __name__ == "__main__":
    install_chinese_fonts()
```

运行字体安装：
```bash
python install_fonts.py
```

### 3.6 启动Jupyter

```bash
# 启动JupyterLab
jupyter lab

# 或启动Jupyter Notebook
jupyter notebook
```

### 3.7 测试安装

创建测试笔记本，运行：
```python
%%manim -qm TestScene

class TestScene(Scene):
    def construct(self):
        # 测试基本图形
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        
        # 测试中文文本
        text = Text("你好，Manim！", font="SimHei").scale(0.8)
        
        self.play(Create(circle))
        self.wait()
        self.play(Transform(circle, square))
        self.wait()
        self.play(Write(text))
        self.wait()
```

---

## 方案四：自建云端服务器部署

### 4.1 服务器要求
- 云服务器（阿里云、腾讯云、AWS等）
- 2核4G内存以上
- Ubuntu 20.04 LTS
- 公网IP

### 4.2 服务器基础配置

#### 连接服务器：
```bash
ssh root@你的服务器IP
```

#### 更新系统：
```bash
apt update && apt upgrade -y
```

#### 安装Docker：
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl start docker
systemctl enable docker
```

### 4.3 部署ManimCE环境

#### 创建部署目录：
```bash
mkdir -p /opt/manim-jupyter
cd /opt/manim-jupyter
```

#### 创建Dockerfile：
```dockerfile
FROM manimcommunity/manim:v0.18.0

USER root

# 安装依赖
RUN apt-get update && apt-get install -y \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    nginx \
    supervisor \
    && apt-get clean

# 安装Python包
RUN pip install --no-cache-dir \
    jupyterlab \
    jupyter-server-proxy \
    nbconvert \
    voila

# 配置Jupyter
RUN jupyter lab --generate-config
COPY jupyter_lab_config.py /root/.jupyter/

# 复制配置文件
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 创建工作目录
RUN mkdir -p /workspace
WORKDIR /workspace

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

#### 创建Jupyter配置：
创建`jupyter_lab_config.py`：
```python
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.allow_root = True
c.ServerApp.token = ''
c.ServerApp.password = ''
c.ServerApp.allow_remote_access = True
```

#### 创建Nginx配置：
创建`nginx.conf`：
```nginx
events {
    worker_connections 1024;
}

http {
    upstream jupyter {
        server 127.0.0.1:8888;
    }
    
    server {
        listen 80;
        server_name _;
        
        location / {
            proxy_pass http://jupyter;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

#### 创建Supervisor配置：
创建`supervisord.conf`：
```ini
[supervisord]
nodaemon=true

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true

[program:jupyter]
command=jupyter lab --config=/root/.jupyter/jupyter_lab_config.py
autostart=true
autorestart=true
user=root
directory=/workspace
```

### 4.4 构建和运行

```bash
# 构建镜像
docker build -t manim-server .

# 运行容器
docker run -d \
  --name manim-jupyter \
  -p 80:80 \
  -v $(pwd)/notebooks:/workspace \
  --restart unless-stopped \
  manim-server
```

### 4.5 配置域名和HTTPS（可选）

#### 安装Certbot：
```bash
apt install certbot python3-certbot-nginx
```

#### 获取SSL证书：
```bash
certbot --nginx -d 你的域名.com
```

### 4.6 设置访问控制

为了安全，可以添加认证：

创建密码文件：
```bash
apt install apache2-utils
htpasswd -c /etc/nginx/.htpasswd 用户名
```

修改nginx配置添加认证：
```nginx
location / {
    auth_basic "Manim Jupyter";
    auth_basic_user_file /etc/nginx/.htpasswd;
    # ... 其他配置
}
```

---

## 常见问题解决

### 5.1 中文字体问题

**问题：** 中文显示为方块或乱码

**解决方案：**
```python
# 方法1：指定字体
text = Text("中文文本", font="SimHei")

# 方法2：配置matplotlib
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 方法3：使用TexTemplate
from manim import TexTemplate
template = TexTemplate()
template.add_to_preamble(r"\usepackage{xeCJK}")
```

### 5.2 FFmpeg相关问题

**问题：** 视频渲染失败

**解决方案：**
```bash
# 检查FFmpeg安装
ffmpeg -version

# 重新安装FFmpeg
# Windows
choco install ffmpeg
# Mac
brew install ffmpeg
# Linux
sudo apt install ffmpeg
```

### 5.3 LaTeX问题

**问题：** 数学公式渲染失败

**解决方案：**
```bash
# 安装完整LaTeX
# Windows: 安装MiKTeX
# Mac: brew install --cask mactex
# Linux: sudo apt install texlive-full

# 配置Manim使用LaTeX
from manim import config
config.tex_template.add_to_preamble(r"\usepackage{amsmath,amsfonts}")
```

### 5.4 内存不足问题

**问题：** 渲染大型动画时内存不足

**解决方案：**
1. 降低视频质量：使用`-ql`代替`-qh`
2. 分段渲染：将长动画拆分为多个场景
3. 增加虚拟内存或升级硬件

### 5.5 权限问题

**问题：** Docker容器权限错误

**解决方案：**
```bash
# 方法1：使用用户命名空间
docker run --user $(id -u):$(id -g) ...

# 方法2：修改文件权限
sudo chown -R $USER:$USER ./notebooks
```

---

## 进阶使用技巧

### 6.1 自定义配置

创建`manim.cfg`配置文件：
```ini
[CLI]
video_dir = ./videos
images_dir = ./images
tex_dir = ./tex
log_dir = ./logs

[render]
fps = 60
resolution = 1080p
```

### 6.2 批量渲染脚本

创建`batch_render.py`：
```python
import os
import subprocess

scenes = [
    ("scene1.py", "Scene1"),
    ("scene2.py", "Scene2"),
    # 添加更多场景
]

for file, scene in scenes:
    cmd = f"manim -qh {file} {scene}"
    print(f"渲染: {scene}")
    subprocess.run(cmd, shell=True)
    print(f"完成: {scene}")
```

### 6.3 自动部署脚本

创建`deploy.sh`：
```bash
#!/bin/bash

# 拉取最新代码
git pull origin main

# 重新构建镜像
docker build -t manim-server .

# 停止旧容器
docker stop manim-jupyter

# 启动新容器
docker run -d \
  --name manim-jupyter \
  -p 80:80 \
  -v $(pwd)/notebooks:/workspace \
  --restart unless-stopped \
  manim-server

echo "部署完成！"
```

### 6.4 监控和日志

#### 查看容器日志：
```bash
docker logs -f manim-jupyter
```

#### 监控资源使用：
```bash
docker stats manim-jupyter
```

#### 设置日志轮转：
```bash
# 在docker run时添加日志配置
--log-driver json-file \
--log-opt max-size=10m \
--log-opt max-file=3
```

---

## 总结

本教程提供了四种不同难度的ManimCE云端编译器搭建方案：

1. **Binder方案**：适合快速体验，零配置
2. **Docker方案**：适合稳定开发，环境一致
3. **Python方案**：适合深度定制，性能最佳
4. **服务器方案**：适合团队协作，专业部署

选择适合您需求的方案，按照教程一步步操作，即可拥有自己的ManimCE云端编译环境！

如果遇到问题，请参考常见问题解决部分，或在GitHub仓库提交Issue。

---

**祝您使用愉快！开始创作精彩的数学动画吧！** 🎬✨
