---
layout: post
title: freemarker应用场景介绍
categories: [java,freemarker]
description: freemarker应用场景介绍
keywords: java,freemarker
---

freemarker应用场景介绍

## freemarker介绍

FreeMarker是一款模板引擎： 即一种基于模板和要改变的数据，并用来生成输出文本（HTML网页、电子邮件、配置文件、源代码等）的通用工具。	它不是面向最终用户的，而是一个Java类库，是一款程序员可以嵌入他们所开发产品的组件。
FreeMarker是免费的，基于Apache许可证2.0版本发布。其模板编写为FreeMarker Template Language（FTL），属于简单、专用的语言。需要准备数据在真实编程语言中来显示，比如数据库查询和业务运算，之后模板显示已经准备好的数据。在模板中，主要用于如何展现数据，而在模板之外注意于要展示什么数据。


## 场景一：动态页面

模板引擎可以让程序实现界面与数据分离，业务代码与逻辑代码的分离，这就提升了开发效率，良好的设计也使得代码复用变得更加容易。<br/>

模板编写为FreeMarkerTemplateLanguage(FTL)。它是简单的，专用的语言，不是像PHP那样成熟的编程语言。那就意味着要准备数据在真实编程语言中来显示，比如数据库查询和业务运算，之后模板显示已经准备好的数据。在模板中，你可以专注于如何展现数据，而在模板之外可以专注于要展示什么数据。<br/>

这种方式通常被称为MVC(模型视图控制器)模式，对于动态网页来说，是一种特别流行的模式。它帮助从开发人员(Java程序员)中分离出网页设计师(HTML设计师)。设计师无需面对模板中的复杂逻辑，在没有程序员来修改或重新编译代码时，也可以修改页面的样式。<br/>
而FreeMarker最初的设计，是被用来在MVC模式的Web开发框架中生成HTML页面的，它没有被绑定到Servlet或HTML或任意Web相关的东西上。它也可以用于非Web应用环境中。

**基于springMVC开发动态页面**

springMVC配置如下`springmvc.xml`
```xml
	<!--视图解释器 -->
	<bean id="viewResolver"
		class="org.springframework.web.servlet.view.freemarker.FreeMarkerViewResolver">
		<property name="contentType" value="text/html; charset=UTF-8" /> 
		<property name="prefix" value="/WEB-INF/ftl/" />
		<property name="suffix" value=".ftl" />
	</bean>
	
	<!-- Freemarker配置 -->
	<bean id="freemarkerConfig"
		class="org.springframework.web.servlet.view.freemarker.FreeMarkerConfigurer">
		<property name="templateLoaderPath" value="/"></property>
		<property name="defaultEncoding" value="UTF-8" />
	</bean>
```
<br/><br/><br/>

编写控制器  HelloWorldController.java
```java
@Controller
public class HelloWorldController {
	
	@RequestMapping("/index")
	public String hellofreemarker(Model model) {
		model.setAttribute("title","Spring MVC And Freemarker");
		model.setAttribute("name","Freemarker");
		return "index";
	}
}
```

编写ftl模板  index.ftl
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>${title}</title>
</head>
<body>
${name}
</body>
</html>
```
访问`http://localhost:8080/index` 即可响应HTML页面

## 场景二：页面静态化

模板 + 数据模型 = 输出，FreeMarker基于设计者和程序员是具有不同专业技能的不同个体的观念，他们是分工劳动的：设计者专注于表示——创建HTML文件、图片、Web页面的其它可视化方面；程序员创建系统，生成设计页面要显示的数据。总之实现了数据与表现的分离。

在`src/main/java/templates`目录下添加名为`product.ftl`的FreeMarker模板，模板的内容如下：

```file
----------产品详细----------
产品名称：${name}
产品价格：${price}
设计作者：<#list users as user> ${user} </#list>
------------------------------
```
模板中一般分为不可变部分与可变部分，如“产品名称：”这些常量内容就是不可以变化的，而`${}`与`<#></#>`这些内容是可以根据数据动态变化的。

<br/><br/><br/><br/><br/><br/>

使用FreeMarker可以读取到模板内容，将数据与模板绑定并渲染出结果，很好的实现了表现与数据分离。新建一个测试类，代码如下：

```java
public class Test {

    public static void main(String[] args) throws Exception {
        
        //创建一个freemarker.template.Configuration实例，它是存储 FreeMarker 应用级设置的核心部分
        //指定版本号
        Configuration cfg=new Configuration(Configuration.VERSION_2_3_22);
        //设置模板目录
        cfg.setDirectoryForTemplateLoading(new File("src/main/java/templates"));
        //设置默认编码格式
        cfg.setDefaultEncoding("UTF-8");
        
        //数据
        Map<String, Object> product = new HashMap<>();
        product.put("name", "Huwei P8");
        product.put("price", "3985.7");
        product.put("users", new String[]{"Tom","Jack","Rose"});
        
        //从设置的目录中获得模板
        Template temp = cfg.getTemplate("product.ftl");
        
        //合并模板和数据模型
        Writer out = new OutputStreamWriter(System.out);
        temp.process(product, out);
        
        //关闭
        out.flush();
        out.close();
    }
}
```
控制台运行运行结果
```console
----------产品详细----------
产品名称：Huwei P8
产品价格：3985.7
设计作者：Tom Jack Rose
------------------------------
```
## 场景三：代码生成器

本文以生成POJO为例

编写模板文件，`pojo.ftl`

<br/><br/><br/>

```ftl
public class ${className}{
	//生成属性
    <#list pos as po>
    private ${po.type} ${po.name};
    </#list>
    //无参构造方法
    public ${className}(){}
	//get 和 set方法
    <#list pos as po>
    public void set${po.name?cap_first}(${po.type!po.name} ${po.name}){
        this.${po.name} = ${po.name};
    }
    public ${po.type!po.name} get${po.name?cap_first}(){
        return this.${po.name};
    }

}
```
新建一个测试类，代码如下：
```java
public class Test {
    public static void main(String[] args) throws Exception {
        Configuration cfg=new Configuration(Configuration.VERSION_2_3_22);       
        cfg.setDirectoryForTemplateLoading(new File("D:/templates"));//设置模板目录 
        cfg.setDefaultEncoding("UTF-8");//设置默认编码格式       
        Map<String, Object> product = new HashMap<>();//数据
        product.put("className", "User");
		List pos = new ArrayList();
		Map<String, Object> po1 = new HashMap<>();
		po1.put("type", "Integer");
		po1.put("name", "id");		
		Map<String, Object> po2 = new HashMap<>();
		po2.put("type", "String");
		po2.put("name", "username");		
		Map<String, Object> po3 = new HashMap<>();
		po3.put("type", "String");
		po3.put("name", "password");
		pos.add(po1); pos.add(po2); pos.add(po3);
        product.put("pos", pos);
        //从设置的目录中获得模板
        Template temp = cfg.getTemplate("pojo.ftl");
        //合并模板和数据模型
        Writer out = new OutputStreamWriter("D:/User.java");
        temp.process(product, out);
        //关闭
        out.flush();
        out.close();
    }
}
```
<br/><br/><br/>

生成的类如下`User.java`
```java
public class User{
	private Integer id;
	private String username;
	private String password;
	public User(){}
	public Integer getId(){
		return id;
	}
	public void setId(Integer id){
		this.id = id;
	}
	public Integer getUsername(){
		return username;
	}
	public void setUsername(String username){
		this.username = username;
	}
	public Integer getPassword(){
		return password;
	}
	public void setPassword(String password){
		this.password = password;
	}
}
```

## 总结：

**freemarker的特征与亮点**

- 功能强大的模板语言：有条件的块，迭代，赋值，字符串和算术运算和格式化，宏和函数，编码等更多的功能；

- 多用途且轻量：零依赖，输出任何格式，可以从任何地方加载模板（可插拔），配置选项丰富；

- 智能的国际化和本地化：对区域设置和日期/时间格式敏感。

- XML处理功能：将dom-s放入到XML数据模型并遍历它们，甚至处理他们的声明

- 通用的数据模型：通过可插拔适配器将java对象暴露于模板作为变量树。

- FreeMarker是免费的，基于Apache许可证2.0版本发布。
