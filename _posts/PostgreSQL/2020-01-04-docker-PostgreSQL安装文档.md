---
layout: post
title: docker-PostgreSQL安装文档
categories: [SQL,PostgreSQL,docker ]
description: docker-Postgres安装文档
keywords: SQL, Postgres,PostgreSQL,docker
---

最强大的开源数据库，PG干O，天天'象'上

## 搜索PostgreSQL镜像

  docker search postgresql

## 下载PostgreSQL镜像

 docker pull docker.io/sameersbn/postgresql

## 启动一个PG容器

docker run --name mypostgres_merry -d -p 5432:5432 -e POSTGRES_PASSWORD=123456 -e PGDATA=/root/pg/data/ -e POSTGRES_USER=admin -e POSTGRES_DB=my_db sameersbn/postgresql

## 进入容器

docker exec -it ${CONTAINER_ID} /bin/bash

## 创建超级管理员

pg默认有超级用户postgres，切换到超级用户
su postgres
\du 查看当前postgresql的用户，一般此时只能看到 postgres
create user admin superuser password '123456';
\du 就可以看到两个用户了。

```psql
postgres=# create user admin superuser password '123456';
CREATE ROLE
postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of
-----------+------------------------------------------------------------+-----------
 admin     | Superuser                                                  | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

postgres=#
```
## 创建数据库

使用超级管理员创建数据，指定数据库的属主
```shell
postgres@6d34ee2c6f32:~$ createdb admindb -O admin
postgres@6d34ee2c6f32:~$ psql
psql (10.9 (Ubuntu 10.9-1.pgdg18.04+1))
Type "help" for help.

postgres=# \l   # 查看当前所有数据库
                             List of databases
   Name    |  Owner   | Encoding | Collate | Ctype |   Access privileges
-----------+----------+----------+---------+-------+-----------------------
 admindb   | admin    | UTF8     | C       | C     |
 my_db     | postgres | UTF8     | C       | C     |
 postgres  | postgres | UTF8     | C       | C     |
 template0 | postgres | UTF8     | C       | C     | =c/postgres          +
           |          |          |         |       | postgres=CTc/postgres
 template1 | postgres | UTF8     | C       | C     | =c/postgres          +
           |          |          |         |       | postgres=CTc/postgres
(5 rows)

postgres=#
```



## 本地登陆数据库

psql --host=127.0.0.1 --username=admin --dbname=admindb --password
输入密码登陆

## **问题**：
此时随便输入密码都能进入，并非bug，而是默认配置如此，需要修改
参考：https://www.cnblogs.com/NolaLi/p/11635078.html
将pg_hba.conf文件的所有trust改为md5,保存重启后，再次登陆需要输入正确密码
```text
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust
host all all 0.0.0.0/0 md5
root@6d34ee2c6f32:/var/lib/postgresql/10/main# cat pg_hba.conf
```
从容器中拷贝出来
docker cp 6d34ee2c6f32:/var/lib/postgresql/10/main/pg_hba.conf ./pg_hba.conf
修改后拷贝进容器中（所有trust改为md5）
docker cp ~/pg_hba.conf 6d34ee2c6f32:/root/pg_hba.conf
移动到正确的目录
mv pg_hba.conf /var/lib/postgresql/10/main/
修改属主和属组
chown postgres:postgres pg_hba.conf
退出容器并重启容器
docker restart 6d34ee2c6f32

再次进入容器并登陆就需要密码，否则不能登陆
```shell
root@6d34ee2c6f32:/var/lib/postgresql# psql --host=127.0.0.1 --username=admin --password --dbname=admindb
Password for user admin:
psql: FATAL:  password authentication failed for user "admin"
root@6d34ee2c6f32:/var/lib/postgresql# psql --host=127.0.0.1 --username=admin --password --dbname=admindb
Password for user admin:
psql (10.9 (Ubuntu 10.9-1.pgdg18.04+1))
Type "help" for help.

admindb=#
```

## 外部用SQL可视化客户端登陆

由于已经做了端口映射，可使用创建的用户密码数据库正常登陆

## 用管理员用户建库和创建普通用户

psql -h 192.168.1.106  -p 5432  -U postgres  

postgres=# create user test01_user with password 'Test01@123';

postgres=# create database test01 owner test01_user;

postgres=# grant all privileges on database test01 to test01_user;
admindb=# grant ALL on database test01 to test01_user;
GRANT
admindb=# grant CREATE on database test01 to test01_user;
GRANT
查看授权帮助
admindb=# \h grant
GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON { [ TABLE ] table_name [, ...]
         | ALL TABLES IN SCHEMA schema_name [, ...] }
    TO role_specification [, ...] [ WITH GRANT OPTION ]
授予 增删改查等 权限 在表和模式上

## 实例

```sql
创建普通用户
create user zhuge with password 'abc@123456';
创建用户的数据库
create database mydb owner zhuge;
授予数据库权限
grant CREATE on database mydb to zhuge;
创建模式
CREATE SCHEMA IF NOT EXISTS junlin;
授予模式权限
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA junlin to zhuge;

创建普通用户
admindb=# create user zhuge with password 'abc@123456';
CREATE ROLE
创建用户的数据库
admindb=# create database mydb owner zhuge;
CREATE DATABASE
在对应数据库中授予用户表创建权限
admindb=# grant CREATE on database mydb to zhuge;
GRANT
退出admin用户
admindb=# \q
使用新用户登录
root@6d34ee2c6f32:/var/lib/postgresql# psql --host=127.0.0.1 --username=zhuge --password --dbname=mydb
Password for user zhuge: 此处输入错误密码，验证密码有效性
psql: FATAL:  password authentication failed for user "zhuge"
root@6d34ee2c6f32:/var/lib/postgresql# psql --host=127.0.0.1 --username=zhuge --password --dbname=mydb
Password for user zhuge:
psql (10.9 (Ubuntu 10.9-1.pgdg18.04+1))
Type "help" for help.
新用户创建模式
mydb=> CREATE SCHEMA IF NOT EXISTS junlin;
CREATE SCHEMA
在对应模式上授予 增删改查 的权限给用户
mydb=> GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA junlin to zhuge;
GRANT
mydb=>
```