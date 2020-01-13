---
layout: post
title: SpringBoot属性读取方式介绍
categories: [java,spring,springboot]
description: SpringBoot属性读取方式介绍
keywords: java,spring,springboot
---

SpringBoot属性读取方式介绍

## 为何需要了解SpringBoot属性读取

伴随着团队的不断壮大，往往不需要开发人员知道测试或者生产环境的全部配置细节，比如数据库密码，帐号信息等。而是希望由运维或者指定的人员去维护配置信息，那么如果要修改某项配置信息，就不得不去修改项目中的文件，导致运维人员又要维护项目代码，造成职责不清，权限不清的问题。

因此可以将配置文件外部化，使用配置文件外部化就需要了解Spring Boot对配置文件的读取方式。

## 直接配置

在src/main/resources下添加配置文件application.properties 
例如修改端口号
```properties
#端口号
server.port=8089
url=http://www.itcast.com
```
直接在代码中注入使用
```java
@Value("${url}")
private String url;

@RequestMapping("/env")
public String env() {
	return url;
}
```
## 使用springboot里面的Environment直接取值

在src/main/resources下配置文件application.properties 添加如下属性
```properties
message.abc=messagefromMQ
```
显示注入， 其次是在需要的地方获取值
```java
@Autowired  
private Environment env; 

public void someMethod(){
	logger.info("===============》 " + env.getProperty("message.abc")); 
}
```
## 对象映射方式读取

在src/main/resources下配置文件application.properties 添加如下属性
```properties
person.name=xiaobai
person.age=18

```
定义配置类：
```java
@Component
@ConfigurationProperties(prefix = "person")    
public class  PersonProperties{  
   private String name;  
   private Integer age;  
 
   // 省列getter setter 方法  
   // ....  
}  
```
## 分环境配置

在src/main/resources下添加，application-pro.properties，application-dev.properties和application.properties三个文件 
1、application.propertie
```properties
spring.profiles.active=dev
```
2、application-pro.properties
```properties
#端口号
server.port=80
#自定义端口号读取
my.name=pzr.dev
```
3、application-dev.properties
```properties
#端口号
server.port=8089
#自定义端口号读取
my.name=pzr.pro
```
当application.propertie设置spring.profiles.active=dev时，则说明是指定使用application-dev.properties文件进行配置

## 自定义配置文件参数读取

@PropertySource配置文件路径设置，在类上添加注解，如果在默认路径下可以不添加该注解 
classpath:config/my.properties指的是src/main/resources目录下config目录下的my.properties文件
多配置文件引用，若取两个配置文件中有相同属性名的值，则取值为最后一个配置文件中的值
```java
@PropertySource({"classpath:config/my.properties","classpath:config/config.properties"})
public class TestController{
	//@Value属性名，在属性名上添加该注解
	@Value("${my.name}")
	private String myName;
}

```

## 总结

springboot读取文件的方式多种多样,总结如下

1.使用@Value注解注入

2.使用@Autowired  Environment对象获取属性 ;

3.使用@ConfigurationProperties(prefix = "person") 给对象属性复制

4.分环境配置spring.profiles.active=dev获取对应配置文件属性

5.使用@PropertySource自定义属性获取

开发者可根据自己的需要选择合适的获取属性的方式。