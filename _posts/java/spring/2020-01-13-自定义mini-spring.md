---
layout: post
title: 自定义mini-spring
categories: [java,spring]
description: 自定义mini-spring
keywords: java,spring
---

自定义mini-springmvc,手写spring核心实现

## 概念

IOC  控制反转(创建对象的权利转移给spring)

DI  依赖注入(有框架给对象设置需要的属性值)   

handlerMapping 处理器映射器   

handlerAdapter  处理器适配器  

DistpatcherServlet 中央控制器 

用到的知识

web中servlet知识

注解

反射

## 依赖

```xml
 <dependencies>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>servlet-api</artifactId>
            <version>2.5</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>



    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.tomcat.maven</groupId>
                <artifactId>tomcat7-maven-plugin</artifactId>
                <version>2.2</version>
                <configuration>
                    <path>/</path>
                    <port>8080</port>
                    <uriEncoding>UTF-8</uriEncoding>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

## 源码

github: https://github.com/zhuliangcai/myproject/tree/master/myspringmvc

```java

package com.springframework.servlet;

import com.springframework.annotaion.*;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Parameter;
import java.net.URL;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * 覆盖 service  init
 */
public class MyDispatcherServlet extends HttpServlet {
    //属性配置容器
    private final Properties myConfig = new Properties();
    //所有需要初始化的类的全限定名
    private final List<String> classNames = new ArrayList<String>();
    //IOC容器 key为id 实例为value
    private final Map<String, Object> ioc = new ConcurrentHashMap<String, Object>();

    //url与方法的映射
    private final Map<String, Method> handlerMap = new ConcurrentHashMap<String, Method>();
    //初始化类加载器
    private ClassLoader defalutClassLoader;

    private final Map<String, Object> controllerMap = new ConcurrentHashMap<String, Object>();


    /**

     */
    @Override
    public void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        //  / ----> 请求了 /soso ----> 请求了
        System.out.println(req.getRequestURI() + " ----> 请求了");

        //5.反射调用方法
        //do service
        doHandler(req,resp);
    }

    private void doHandler(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException{
        String requestURI = req.getRequestURI();

        if(!handlerMap.containsKey(requestURI)){
            resp.getWriter().write("404 "+requestURI+ " not Found !");
            return;
        }

        Method method = handlerMap.get(requestURI);
        //这里需要方法所在的类对象 , 需要有一个 url 与 Controller的映射关系容器
        Map parameterMap = req.getParameterMap();
        System.out.println("参数:"+parameterMap);
        try {
            Parameter[] parameters = method.getParameters();

            Class<?>[] parameterTypes = method.getParameterTypes();
            Object[] params = new Object[parameterTypes.length];
            for(int i=0;i<parameterTypes.length;i++){
                Class<?> type = parameterTypes[i];
                System.out.println(type);
                if(type == HttpServletRequest.class){
                    params[i]=req;
                }else if(type == HttpServletResponse.class){
                    params[i]=resp;
                }else if(type == String.class){
                    String name = parameters[i].getName();
                    System.out.println("参数名称"+name);
                    //粗略处理
                    RequestParam requestParam = parameters[i].getAnnotation(RequestParam.class);
                    System.out.println("注解属性名:"+requestParam.value());
                    params[i] = req.getParameter(requestParam.value());
                }else {
                    continue;
                }
            }

            Object invoke = method.invoke(controllerMap.get(requestURI), params);
            resp.getWriter().write(invoke.toString());
            return;
        }  catch (Exception e) {
            e.printStackTrace();
            resp.getWriter().write("500: "+Arrays.toString(e.getStackTrace()));
            return;
        }


    }

    /**
     * 获取配置文件
     */
    @Override
    public void init(ServletConfig config) throws ServletException {
        System.out.println("初始化了");

        //1.加载属性文件
        initConfig(config);

        String scanPackage = myConfig.getProperty("scanPackage");
        //2.扫描包
        doScanPackage(scanPackage);

        //3.IOC容器 利用反射实例化对象
        doInstance();

        //4.DI依赖注入
        doAutowired();

        //5.url与方法建立映射
        doHandlerMapping();

        System.out.println(handlerMap);
        System.out.println(controllerMap);

        //6.反射调用方法
        //do service
        //初始化完成
        System.out.println("初始化完成 init ok ......");
//        执行service方法


    }

    //5.url与方法建立映射
    private void doHandlerMapping() {

        Collection<Object> values = ioc.values();
        for(Object o : values){

            //如果不是带有Controller注解的类不做处理
            if(!o.getClass().isAnnotationPresent(Controller.class)){
                continue;
            }
            String head ="/";
            if(o.getClass().isAnnotationPresent(RequestMapping.class)){
                RequestMapping classMapping = o.getClass().getAnnotation(RequestMapping.class);
                head += classMapping.value();
            }

            //建立映射关系
            Method[] declaredMethods = o.getClass().getDeclaredMethods();
            for(Method m:declaredMethods){
                //如果没有RequestMapping,不做处理
                if(!m.isAnnotationPresent(RequestMapping.class)){
                    continue;
                }

                //建立url映射method关系

                RequestMapping annotation = m.getAnnotation(RequestMapping.class);


                String url = head +"/"+annotation.value();
                //把所有的 多个 "///" 替换成一个 /
                handlerMap.put(url.replaceAll("/+","/"),m);
                controllerMap.put(url.replaceAll("/+","/"),o);

            }

        }



    }

    private void doAutowired() throws ServletException{
        Collection<Object> values = ioc.values();
        for(Object o : values){
            Field[] declaredFields = o.getClass().getDeclaredFields();
            for(Field f: declaredFields){
                if(f.isAnnotationPresent(Autowired.class)){
                    f.setAccessible(true);

                    String className = f.getName();
                    System.out.println(o + "-----注入Autowired-----" +f.getName());

                    try {
                        f.set(o,ioc.get(f.getName()));
                    } catch (IllegalAccessException e) {
                        e.printStackTrace();
                        throw new ServletException("500 :" + className + " not found! doInstance ERROR!" + Arrays.toString(e.getStackTrace()));
                    }
                }
            }
        }
        System.out.println("ioc ok" + ioc);
    }

    //递归扫描包,根据注解实例化对象保存到IOC容器中
    private void doInstance() throws ServletException{
        for(int i=0;i<classNames.size();i++){
            String className = classNames.get(i);

            try {
                Class<?> clazz = Class.forName(className);
                String simpleName = lowerCaseFirst(clazz.getSimpleName());
//
                if(clazz.isAnnotationPresent(Controller.class)){
                    Controller annotation = clazz.getAnnotation(Controller.class);
                    if(!"".equals(annotation.value())){
                        simpleName=annotation.value();
                    }
                    ioc.put(simpleName,clazz.newInstance());

                }else if(clazz.isAnnotationPresent(Service.class)){
                    Service annotation = clazz.getAnnotation(Service.class);
                    if(!"".equals(annotation.value())){
                        simpleName=annotation.value();
                    }
                    Object service = clazz.newInstance();
                    ioc.put(simpleName,service);
                    Class<?>[] interfaces = clazz.getInterfaces();
                    for(Class in : interfaces){
                        ioc.put(lowerCaseFirst(in.getSimpleName()),service);
                    }

                }else{
                    continue;
                }




            } catch (Exception e) {
                e.printStackTrace();
                throw new ServletException("500 :" + className + " not found! doInstance ERROR!" + Arrays.toString(e.getStackTrace()));
            }

        }
    }

    //首字母转小写
    private String lowerCaseFirst(String simpleName) {
        char[] chars = simpleName.toCharArray();
        int c = chars[0];
        chars[0]=(char)(c+32);
        return new String(chars);
    }

    private void doScanPackage(String scanPackage) {
        String folder = scanPackage.replaceAll("\\.", "/");
        System.out.println(folder);
        //根据包获取文件夹
        URL url = defalutClassLoader.getResource(folder);

        System.out.println("doScanPackage:" +scanPackage+"---->"+url);
        File file = new File(url.getFile());

        //递归获取
        for (File f:file.listFiles() ) {
            if(f.isDirectory()){
                doScanPackage(scanPackage + "."+f.getName());
            }else if(f.isFile() && f.getName().endsWith(".class")){
                //获取到类文件
                classNames.add(scanPackage + "."+f.getName().replace(".class",""));
            }else {
                continue;
            }
        }

    }

    private void initConfig(ServletConfig config) throws ServletException {
        defalutClassLoader = this.getClass().getClassLoader();
        //初始化了
        //app.conf
        //获取配置文件
        String configuationName = config.getInitParameter("configuationName");
        System.out.println(configuationName);
        InputStream inputStream = defalutClassLoader.getResourceAsStream(configuationName);
        try {
            myConfig.load(inputStream);
        } catch (IOException e) {
            e.printStackTrace();
            throw new ServletException("500 :" + configuationName + " not exist! init ERROR!" + Arrays.toString(e.getStackTrace()));
        }
    }
}

```

