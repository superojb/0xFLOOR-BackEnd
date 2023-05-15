## 环境搭建

### Docker
```shell
# apt包列表完全更新
apt-get update -y
# 安装Get
apt install git
# 安裝Docker
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
service docker start

# 开机自启
sudo systemctl enable docker
```

### Python
```shell
docker run -it -d --name=Backend -p 80:80 -v /home/backend:/home/backend python:3.9.0 bash

docker exec -it Backend /bin/bash
cd /home/backend/

apt-get update -y
apt-get install vim
```

### python 依赖
```shell
pip install Django==3.2.18
pip install django-rest-auth==0.9.5
pip install django-allauth==0.40.0
pip install django-filter==2.4.0
pip install cryptography
pip install drf-yasg
pip install python3-openid
pip install pymysql
pip install tronpy
pip install loguru

```

### 数据库
```shell
docker run \
--restart=always -d \
--name mysql \
-p 3306:3306 \
-v /home/mysql/conf.d/:/etc/mysql/conf.d \
-v /home/mysql/mysql/:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql
  
docker exec -it mysql /bin/bash

mysql -hlocalhost -uroot -p123456

# 两个docker 建立连接
docker network create -d bridge network1
docker network connect network1 mysql
docker network connect network1 Backend

apt install iputils-ping
ping mysql
# 看IP
```

### 创建超级管理员
```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 报错
1. pymysql报错：cryptography is required for sha256_password or caching_sha2_password
```shell
# 其实 cryptography 是一个python包，所以解决方法很简单
pip install cryptography
```

1. ImportError: cannot import name 'FieldDoesNotExist' from 'django.db.models' 
```shell
vi /usr/local/lib/python3.9/site-packages/allauth/utils.py

# from django.db.models import FieldDoesNotExist, FileField
# 换成
# from django.core.exceptions import FieldDoesNotExist
```

```shell
python manage.py runserver 0.0.0.0:80

```