---
layout: post
title: dubbo涉及的技术
categories: Blog
description: dubbo涉及技术汇总。
keywords: 逐步学习
---

框架设计只精妙,都在于作者阅历之丰厚。

# RPC
基本原理
![](/images/posts/RPC-basic.png)

# SPI
    SPI 全称为 Service Provider Interface，是一种服务发现机制。SPI 的本质是将接口实现类的全限定名配置在文件中，并由服务加载器读取配置文件，加载实现类。这样可以在运行时，动态为接口替换实现类。
    Java SPI 和 Dubbo SPI 

# 自适应拓展机制
    代码生成，通过AdaptiveClassCodeGenerator生成中间代理类，再中间类中使用ExtensionLoader加在对应的拓展类，主要注解Activate

# Jdk动态代理
    主要类和接口 InvocationHandler Proxy.newProxyInstance()
    通过dubbo获取的用户服务类都已经使用了Jdk动态代理生成了代理类

# 集群和负载均衡
    分组和版本控制，集群容错
    权重随机，最少活跃调用数，一致性哈希，权重轮询

# zookeeper
    ZooKeeper是一个分布式的，开放源码的分布式应用程序协调服务，是Google的Chubby一个开源的实现，是Hadoop和Hbase的重要组件。它是一个为分布式应用提供一致性服务的软件，提供的功能包括：配置维护、域名服务、分布式同步、组服务等。
    在dubbo中主要用于服务注册与发现，配置中心和路由

# 网络编程框架 netty3 netty4 mina grizzly
    Netty是由JBOSS提供的一个java开源框架，现为 Github上的独立项目。Netty提供异步的、事件驱动的网络应用程序框架和工具，用以快速开发高性能、高可靠性的网络服务器和客户端程序。

# javassit
    Javassist是一个开源的分析、编辑和创建Java字节码的类库。是由东京工业大学的数学和计算机科学系的 Shigeru Chiba （千叶 滋）所创建的。它已加入了开放源代码JBoss 应用服务器项目，通过使用Javassist对字节码操作为JBoss实现动态"AOP"框架。

# 线程池，阻塞队列，动态代理，代码生成，内存编译


