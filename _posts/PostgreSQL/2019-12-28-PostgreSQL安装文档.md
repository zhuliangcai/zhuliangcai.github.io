---
layout: post
title: PostgreSQL安装文档
categories: [SQL]
description: Postgres安装文档
keywords: SQL, Postgres,PostgreSQL
---

最强大的开源数据库，PG干O，天天'象'上


# PostgreSQL安装文档

[官网地址]: https://www.postgresql.org/
[下载地址]: https://www.postgresql.org/ftp/source/

![2019-08-10_110114.png](https://i.loli.net/2019/08/10/EIeYymRcJgQkVs5.png)

### 下载源码

选择需要的版本，下载获取源码

![2019-08-10_110247.png](https://i.loli.net/2019/08/10/9bwBeryjQOuFRSq.png)

### 安装命令

```shell
./configure --with-readline #命令提示不全
gmake
sudo su
gmake install
mkdir /usr/local/pgsql/data 
chown kduser /usr/local/pgsql/data
exit
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data  # 初始化数据库目录
/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data >logfile 2>&1 &

[kduser@v-k8s-smartpos postgresql-9.3.25]$ /usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data > logfile 2>&1 &   # 启动服务

/usr/local/pgsql/bin/createdb test # 创建数据库
/usr/local/pgsql/bin/psql test # 连接数据库
[kduser@v-k8s-smartpos postgresql-9.3.25]$ /usr/local/pgsql/bin/psql test
psql (9.3.25)
Type "help" for help.

test=# help
You are using psql, the command-line interface to PostgreSQL.
Type:  \copyright for distribution terms
       \h for help with SQL commands
       \? for help with psql commands
       \g or terminate with semicolon to execute query
       \q to quit
test=#

```

### 设置pgsql Home

```shell
export JAVA_HOME=/usr/local/jdk1.8
export PATH=$PGSQL_HOME/bin:$PATH
```

### 简单的后台启动命令

```shell
pg_ctl start -l logfile # postgresql-doc.pdf 573页 因此我们提供了封装程序 pg_ctl以简化一些任务
# 参考帮助，可以初始化，启动，停止，控制 PostgreSQL服务
[kduser@v-k8s-smartpos ~]$ pg_ctl --help
pg_ctl is a utility to initialize, start, stop, or control a PostgreSQL server.

Usage:
  pg_ctl init[db]               [-D DATADIR] [-s] [-o "OPTIONS"]
  pg_ctl start   [-w] [-t SECS] [-D DATADIR] [-s] [-l FILENAME] [-o "OPTIONS"]
  pg_ctl stop    [-W] [-t SECS] [-D DATADIR] [-s] [-m SHUTDOWN-MODE]
  pg_ctl restart [-w] [-t SECS] [-D DATADIR] [-s] [-m SHUTDOWN-MODE]
                 [-o "OPTIONS"]
  pg_ctl reload  [-D DATADIR] [-s]
  pg_ctl status  [-D DATADIR]
  pg_ctl promote [-D DATADIR] [-s]
  pg_ctl kill    SIGNALNAME PID

Common options:
  -D, --pgdata=DATADIR   location of the database storage area
  -s, --silent           only print errors, no informational messages
  -t, --timeout=SECS     seconds to wait when using -w option
  -V, --version          output version information, then exit
  -w                     wait until operation completes
  -W                     do not wait until operation completes
  -?, --help             show this help, then exit
(The default is to wait for shutdown, but not for start or restart.)
....
```

### postgresql 查看当前用户名

```sql
test=# select * from current_user;
 current_user
--------------
 kduser
(1 row)
--修改密码
 ALTER USER kduser WITH PASSWORD '123456';

```

### PostgreSQL9.3 设置允许通过IP进行访问

```bug
 FATAL:  no pg_hba.conf entry for host "172.20.155.43", user "kduser", database "test"
```

修改 PostgreSQL安装目录\data 下的两个配置文件pg_hba.conf和postgresql.conf。

1、修改pg_hba.conf文件中的80行，将【127.0.0.1】修改成安装PostgreSQL电脑的IP

32指代本地网段，24指代外部网段

```shell
host    all             all             172.20.183.0/24            md5
```

2、修改postgresql.conf文件中的59行，将【*】修改成安装PostgreSQL电脑的IP

```shell
listen_addresses = '172.20.183.184'
```



### 安装中文分析器
    
    参考统计目录下文档： PostgreSQL中文分词zhpaser.md
    

### 启动
切换到非 root 用户。（PgSQL 在安装完毕后会创建一个名为 postgres 的超级用户，我们可以使用这个超级用户来操作 PgSQL，后期建议重新创建一个普通用户用来管理数据）；
切换到 /installPath/bin/ 目录下，PgSQL 在此目录下提供了很多命令，如 createdb、createuser、dropdb、pg_dump等；
使用 createdb 命令初始化一个文件夹 dir_db (此目录不能已存在)存放数据库物理数据，使用 -E UTF8 参数指定数据库字符集为 utf-8；
使用 pg_ctl -D dir_db 指定数据库启动后台服务；
使用 psql -d db 在命令行登陆 PgSQL;



