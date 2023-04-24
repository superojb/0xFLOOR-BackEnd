## 环境搭建

### python 依赖
```shell
pip install Django==3.2.18
pip install django-rest-auth==0.9.5
pip install django-allauth==0.40.0
pip install django-filter==2.4.0
pip install cryptography
pip install drf-yasg
pip install python3-openid
```

### 创建超级管理员
```shell
python manage.py createsuperuser
```

### Mysql 配置
https://blog.csdn.net/qq_38890412/article/details/102884696


### 报错
1. pymysql报错：cryptography is required for sha256_password or caching_sha2_password
```shell
# 其实 cryptography 是一个python包，所以解决方法很简单
pip install cryptography
```