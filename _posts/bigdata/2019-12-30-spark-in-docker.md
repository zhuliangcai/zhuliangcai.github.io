---
layout: post
title: docker中使用spark
categories: [docker,spark,容器]
description: docker中使用spark
keywords: docker,spark,容器
---

docker中使用spark

## 安装

 docker pull docker.io/sequenceiq/spark

## 启动spark容器命令
```shell
 docker run -it -p 8088:8088 -p 8042:8042 -h sandbox docker.io/sequenceiq/spark bash
```

## 进入容器命令

```shell
docker exec -it blissful_rosalind  bash

```
## 启动master服务进程
```shell
 /usr/local/spark/sbin/start-master.sh
```

## 启动spark-shell
```shell
 spark-shell master=spark://sandbox:7077  成功
 
spark-shell \
--master yarn-client \
--driver-memory 1g \
--executor-memory 1g \
--executor-cores 1
```

## 测试

```shell
 sc.parallelize(1 to 1000).count  计数
```
## wordcount 
```shell
sc.textFile("file:///text.txt").flatMap(_.split("[ ,.?;]")).map((_,1)).reduceByKey(_+_).sortByKey().collect
```


```shell

```



```shell

```