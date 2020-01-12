---
layout: post
title: 注册bat为windows服务
categories: [bat,windows,注册,服务]
description: 注册bat为windows服务
keywords: bat,windows,注册,服务
---

将BAT文件注册为windows服务的方法

## 第一步：

    下载微软系统小工具 instsrv.exe和srvany.exe至C:\Windows\System32。
## 第二步：

    运行Dos命令代码：instsrv ServiceName C:\Windows\System32\srvany.exe    
    (ServiceName 即你自己定义的服务名称，可以是要作为系统服务启动的应用程序的名称。) 

## 第三步：

    打开注册表，定位到下面的路径。 
    HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ServiceName 
    (同样的ServiceName是你刚才安装服务时自定义的服务名称。) 
    如果该服务名下没有Parameters项目，则对服务名称项目右击新建项，名称为Parameters，然后定位到Parameters项，新建以下几个字符串值。 
    名称 Application 值为你要作为服务运行的BAT文件地址。 
    名称 AppDirectory 值为你要作为服务运行的BAT文件所在文件夹路径。 
    名称 AppParameters 值为你要作为服务运行的BAT文件启动所需要的参数。 

## 注：

instsrv ServiceName remove 命令可删除服务。

## 参考: 

https://blog.csdn.net/LAI515/article/details/89341591