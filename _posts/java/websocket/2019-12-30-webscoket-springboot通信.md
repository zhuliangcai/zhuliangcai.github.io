---
layout: post
title: webscoket-springboot通信
categories: [webscoket,springboot,通信,协议]
description: webscoket-springboot通信
keywords: webscoket,springboot,通信
---

这次给大家说一下自己对websocket + spring boot结合使用的一些经验

## websocket是什么

首先websocket是一个持久化的协议，实现了浏览器与服务器的全双工通信。不再像http那样，只有在浏览器发出request之后才有response，websocket能实现服务器主动向浏览器发出消息。

## pom依赖

下面我们用spring boot来实现一下：

在spring boot的文档中，介绍了我们需要配置的文件
pom.xml
```xml
<dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-websocket</artifactId>
</dependency>
```
## 配置类

之后我们需要添加一个单例bean，名为ServerEndpointExporter
```java
@Configuration
public class WebSocketConfig {
    @Bean
    public ServerEndpointExporter serverEndpointExporter (){
        return new ServerEndpointExporter();
    }
}
```

## 通信类

接下来便能使用websocket了，下面是一个简单的例子：
```java
@ServerEndpoint("/websocket")
@Component
public class MyWebSocket {
 
    private static int onlineCount = 0;
 
    private static CopyOnWriteArraySet<MyWebSocket> webSocketSet = new CopyOnWriteArraySet<>();
 
    private Session session;
 
    @OnOpen
    public void onOpen (Session session){
        this.session = session;
        webSocketSet.add(this);
        addOnlineCount();
        System.out.println("有新链接加入!当前在线人数为" + getOnlineCount());
    }
 
    @OnClose
    public void onClose (){
        webSocketSet.remove(this);
        subOnlineCount();
        System.out.println("有一链接关闭!当前在线人数为" + getOnlineCount());
    }
 
    @OnMessage
    public void onMessage (String message, Session session) throws IOException {
        System.out.println("来自客户端的消息:" + message);
        // 群发消息
        for ( MyWebSocket item : webSocketSet ){
                item.sendMessage(message);
        }
    }
 
    public void sendMessage (String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }
 
    public static synchronized  int getOnlineCount (){
        return MyWebSocket.onlineCount;
    }
 
    public static synchronized void addOnlineCount (){
        MyWebSocket.onlineCount++;
    }
 
    public static synchronized void subOnlineCount (){
        MyWebSocket.onlineCount--;
    }
 
}
```

## HTML&JS

代码很简单，相信大家都能看懂，接下来贴一下html代码：

```html
<!DOCTYPE HTML>
<html>
<head>
    <base href="localhost://localhost:8080/">
    <title>My WebSocket</title>
</head>
 
<body>
Welcome<br/>
<input id="text" type="text"/>
<button onclick="send()">Send</button>
<button onclick="closeWebSocket()">Close</button>
<div id="message">
</div>
</body>
 
<script type="text/javascript">
    var websocket = null;
 
    //判断当前浏览器是否支持WebSocket
    if ('WebSocket' in window) {
        websocket = new WebSocket("ws://localhost:8080/websocket");
    }
    else {
        alert('Not support websocket')
    }
 
    //连接发生错误的回调方法
    websocket.onerror = function () {
        setMessageInnerHTML("error");
    };
 
    //连接成功建立的回调方法
    websocket.onopen = function (event) {
        setMessageInnerHTML("open");
    }
 
    //接收到消息的回调方法
    websocket.onmessage = function (event) {
        setMessageInnerHTML(event.data);
    }
 
    //连接关闭的回调方法
    websocket.onclose = function () {
        setMessageInnerHTML("close");
    }
 
    //监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
    window.onbeforeunload = function () {
        websocket.close();
    }
 
    //将消息显示在网页上
    function setMessageInnerHTML(innerHTML) {
        document.getElementById('message').innerHTML += innerHTML + '<br/>';
    }
 
    //关闭连接
    function closeWebSocket() {
        websocket.close();
    }
 
    //发送消息
    function send() {
        var message = document.getElementById('text').value;
        websocket.send(message);
    }
</script>
</html>
```

## 测试

接下来便能直接启动websocket进行访问了，具体的扩展可以根据你的业务需求进行增加。
其实websocket就是基于http协议的升级，在http的headers中有一个header名为Upgrade，用来对http协议进行升级，从而换用其他的协议，在本例中，为Upgrade:websocket

