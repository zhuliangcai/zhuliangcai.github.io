---
layout: post
title: spring boot+mybatis plus快速入门
categories: [java,spring,springboot,mybatis]
description: spring boot+mybatis plus快速入门
keywords: java,spring,springboot,mybatis
---

spring boot+mybatis plus快速入门

## 前言

  对于springboot项目，mybatis plus团队也有自己的启动器 ：mybatis-plus-boot-starter。这个依赖内部已经整合了mybatis-spring，也包括非快速启动的mybatis-plus（这个依赖需要额外的配置数据源等信息），所以如果您在网上看到引入两个和mybatis-plus有关的依赖的话完全是多余的。

## 一、创建spring boot项目

首先创建一个spring boot项目 ,先创建基本的maven项目工程,在创建项目时直接引入最基本的两个依赖： 

```xml
spring-boot-starter-web
mysql-connector-java
```

## 二、添加整合的依赖

接着再去引一下阿里的fastjson，以及模板生成需要的freemarker。最重要的，我们需要引入mybatis-plus-boot-starter依赖（可以从maven库找到）

此处选用2.2.0版本的mybatis-plus-boot-starter启动器：

```xml
mybatis-plus-boot-starter
freemarker
fastjson
```

pom依赖全部完毕, 完整pom.xml如下 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.test</groupId>
    <artifactId>springboot-mybatisplus</artifactId>
    <version>1.0-SNAPSHOT</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.3.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>
        <!-- https://mvnrepository.com/artifact/com.baomidou/mybatis-plus-boot-starter -->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>2.2.0</version>
        </dependency>
        <!-- freemarker -->
        <dependency>
            <groupId>org.freemarker</groupId>
            <artifactId>freemarker</artifactId>
        </dependency>
        <!-- fastjson -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.15</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

说明：可以看到，包括web依赖和mysql驱动依赖，总共就添加了五个依赖。当然，此处也只是一个Demo样例，并未添加阿里的Druid连接池，但是完全不会影响我们实现大量而基本的持久层操作。 

## 三、spring boot数据源配置

这个不说废话，直接上完整application.properties文件：

```properties
server.port=8080
#datasource
spring.datasource.url=jdbc:mysql://localhost:3306/mybatis?useUnicode=true&characterEncoding=utf8
spring.datasource.username=root
spring.datasource.password=123456
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
```

## 四、生成代码

表语句

```sql
CREATE TABLE `user` (
  `id` bigint(20) NOT NULL COMMENT '主键ID',
  `name` varchar(30) DEFAULT NULL COMMENT '姓名',
  `age` int(11) DEFAULT NULL COMMENT '年龄',
  `email` varchar(50) DEFAULT NULL COMMENT '邮箱',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
```

生成代码工具类

```java
package com.test.springboot.mybatisplus.generate;

import com.baomidou.mybatisplus.generator.AutoGenerator;
import com.baomidou.mybatisplus.generator.config.DataSourceConfig;
import com.baomidou.mybatisplus.generator.config.GlobalConfig;
import com.baomidou.mybatisplus.generator.config.PackageConfig;
import com.baomidou.mybatisplus.generator.config.StrategyConfig;
import com.baomidou.mybatisplus.generator.config.converts.MySqlTypeConvert;
import com.baomidou.mybatisplus.generator.config.rules.DbColumnType;
import com.baomidou.mybatisplus.generator.config.rules.DbType;
import com.baomidou.mybatisplus.generator.config.rules.NamingStrategy;
import com.baomidou.mybatisplus.generator.engine.FreemarkerTemplateEngine;

/**
 * <p>
 * 代码生成器演示
 * </p>
 */
public class MpGenerator {

    public static void main(String[] args) {
//        assert (false) : "代码生成属于危险操作，请确定配置后取消断言执行代码生成！";
        AutoGenerator mpg = new AutoGenerator();
        // 选择 freemarker 引擎，默认 Velocity
        mpg.setTemplateEngine(new FreemarkerTemplateEngine());

        // 全局配置
        GlobalConfig gc = new GlobalConfig();
        gc.setAuthor("Mht");
        gc.setOutputDir("C:\\Users\\MR\\Desktop\\springboot-mybatisplus\\src\\main\\java");
        gc.setFileOverride(false);// 是否覆盖同名文件，默认是false
        gc.setActiveRecord(true);// 不需要ActiveRecord特性的请改为false
        gc.setEnableCache(false);// XML 二级缓存
        gc.setBaseResultMap(true);// XML ResultMap
        gc.setBaseColumnList(false);// XML columList

        mpg.setGlobalConfig(gc);

        // 数据源配置
        DataSourceConfig dsc = new DataSourceConfig();
        dsc.setDbType(DbType.MYSQL);
        dsc.setTypeConvert(new MySqlTypeConvert() {
            // 自定义数据库表字段类型转换【可选】
            @Override
            public DbColumnType processTypeConvert(String fieldType) {
                System.out.println("转换类型：" + fieldType);
                // 注意！！processTypeConvert 存在默认类型转换，如果不是你要的效果请自定义返回、非如下直接返回。
                return super.processTypeConvert(fieldType);
            }
        });
        dsc.setDriverName("com.mysql.jdbc.Driver");
        dsc.setUsername("root");
        dsc.setPassword("123456");
        dsc.setUrl("jdbc:mysql://localhost:3306/mybatis?useUnicode=true&characterEncoding=utf8");
        mpg.setDataSource(dsc);

        // 策略配置
        StrategyConfig strategy = new StrategyConfig();

        strategy.setNaming(NamingStrategy.nochange);// 表名生成策略
        strategy.setInclude(new String[]{"user"}); // 需要生成的表

        mpg.setStrategy(strategy);

        // 包配置
        PackageConfig pc = new PackageConfig();
        pc.setParent("com.test.springboot.mybatisplus");
        mpg.setPackageInfo(pc);


        // 执行生成
        mpg.execute();
    }
}

```

注意事项：
需要更改的地方有：文件输出路径（根据项目需要定制），数据源（此类是单独的数据库反向生成代码执行文件，因此springboot的数据源不起作用），包配置. 

执行，刷新，获得自动生成的业务代码 

##五、添加spring boot启动类

```java
package com.test;

import org.mybatis.spring.annotation.MapperScan;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.test.springboot.mybatisplus.mapper")
public class SpringBootMybatisPlusApplication {
    private static final Logger logger = LoggerFactory.getLogger(SpringBootMybatisPlusApplication.class);

    public static void main(String[] args) {
        SpringApplication.run(SpringBootMybatisPlusApplication.class, args);
        logger.info("========================启动完毕========================");
    }
}

```

## 六、编写controller类

```java
package com.test.springboot.mybatisplus.web;


import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.plugins.Page;
import com.test.springboot.mybatisplus.entity.User;
import com.test.springboot.mybatisplus.service.IUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RestController;

/**
 * <p>
 * 前端控制器
 * </p>
 */
@RestController
@RequestMapping("/user")
public class UserController {
    @Autowired
    private IUserService userSvc;

    @GetMapping(value = "/show")
    public JSONObject testEnum() {
        Page<User> users = userSvc.selectPage(new Page<>(1, 10));
        JSONObject result = new JSONObject();
        result.put("users", users);

        return result;
    }
}
```

说明：mybatis-plus已经为我们将基本的crud操作封装以待，在代码生成的过程中我们也已经看到UserMapper接口自动继承了BaseMapper接口，它里面有丰富的接口方法且已经按照常规的开发习惯实现完毕，虽然我们的Mapper接口中一个方法都没有，却可以实现大部分crud操作。

## 七、测试

打开浏览器发送get请求:  http://localhost:8080/user/show 

结果:

```json
{"users":{"total":0,"size":10,"pages":0,"current":1,"records":[{"id":1,"name":"Jone","age":18,"email":"test1@baomidou.com"},{"id":2,"name":"Jack","age":20,"email":"test2@baomidou.com"},{"id":3,"name":"Tom","age":28,"email":"test3@baomidou.com"},{"id":4,"name":"Sandy","age":21,"email":"test4@baomidou.com"},{"id":5,"name":"Billie","age":24,"email":"test5@baomidou.com"},{"id":1136795099968077825,"name":"lombok","age":19,"email":"lombok@123.com"},{"id":1136795381292597249,"name":"lombok","age":19,"email":"lombok@123.com"}]}}
```

## 总结

通读全文，我们轻松实现了自己的mybatis持久层整合操作。不得不说mybatis-plus真的非常不错, 简单，高效，使用起来清晰易懂。