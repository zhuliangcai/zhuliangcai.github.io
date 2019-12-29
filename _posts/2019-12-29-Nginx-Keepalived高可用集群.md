---
layout: post
title: Nginx+Keepalived高可用集群
categories: [nginx,keepalived,高可用,集群]
description: Nginx+Keepalived高可用集群
keywords: nginx,keepalived,高可用,集群
---

Nginx+Keepalived高可用集群

# Nginx+Keepalived高可用集群

**1.Keepalived高可用软件**

​    Keepalived软件起初是专为LVS负载均衡软件设计的，用来管理并监控LVS集群系统中各个服务节点的状态，后来又加入了可以实现高可用的VRRP功能。因此，keepalived除了能够管理LVS软件外，还可以作为其他服务的高可用解决方案软件。

​    keepalived软件主要是通过VRRP协议实现高可用功能的。VRRP是Virtual  Router  Redundancy Protocol（虚拟路由冗余协议）的缩写，VRRP出现的目的就是为了解决静态路由的单点故障问题的，它能保证当个别节点宕机时，整个网络可以不间断地运行。所以，keepalived一方面具有配置管理LVS的功能，同时还具有对LVS下面节点进行健康检查的功能，另一方面也可以实现系统网络服务的高可用功能。

**2.Keepalived高可用故障切换转移原理**

​    Keepalived高可用服务对之间的故障切换转移，是通过VRRP来实现的。在keepalived服务工作时，主Master节点会不断地向备节点发送（多播的方式）心跳消息，用来告诉备Backup节点自己还活着。当主节点发生故障时，就无法发送心跳的消息了，备节点也因此无法继续检测到来自主节点的心跳了。于是就会调用自身的接管程序，接管主节点的IP资源和服务。当主节点恢复时，备节点又会释放主节点故障时自身接管的IP资源和服务，恢复到原来的备用角色。

**3. Keepalived高可用实验环境说明**

​    如下图所示，前端有两台的Nginx负载均衡器，用来分发接收到客户端的请求。在前文已经配置好了Nginx01，Nginx02也是一样的配置。现在要在两个Nginx负载均衡器上做高可用配置，Nginx01作为主节点，Nginx02作为备节点。

![image.png](http://s1.51cto.com/images/20180407/1523083612988586.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=) 

**4.安装并启用keepalived**

​    keepalived的安装非常简单，直接使用yum来安装即可。

```
 yum install keepalived -y
```

​    安装之后，启动keepalived服务，顺便把keepalived写入开机启动的脚本里面去。。

```
/etc/init.d/keepalived start
echo "/etc/init.d/keepalived start" >>/etc/rc.local
```

​    启动之后会有三个进程，没问题之后可以关闭keepalived软件，接下来要修改keepalived的配置文件。

![image.png](http://s1.51cto.com/images/20180407/1523068336960962.png?x-oss-process=image/watermark,size_16,text_QDUxQ1RP5Y2a5a6i,color_FFFFFF,t_100,g_se,x_10,y_10,shadow_90,type_ZmFuZ3poZW5naGVpdGk=)

5.修改keepalived配置文件并且重启keepalived服务

```
/etc/init.d/keepalived stop    #关闭keepalived服务   
vim /etc/keepalived/keepalived.conf  #用vim打开编辑
```

| 主节点的配置文件                                             | 备节点的配置文件                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ! Configuration File for keepalived global_defs {   notification_email {     acassen@firewall.loc     failover@firewall.loc     sysadmin@firewall.loc   }   notification_email_from Alexandre.Cassen@firewall.loc   smtp_server 192.168.200.1   smtp_connect_timeout 30   router_id **lb01**} vrrp_instance VI_1 {    state **MASTER**    interface **eth1**    virtual_router_id **55**    priority **150**    advert_int 1    authentication {        auth_type PASS        auth_pass **123456**    }    virtual_ipaddress {        **192.168.31.5/24 dev eth1 label eth1:1**    }}...... | ! Configuration File for keepalived global_defs {   notification_email {     acassen@firewall.loc     failover@firewall.loc     sysadmin@firewall.loc   }   notification_email_from Alexandre.Cassen@firewall.loc   smtp_server 192.168.200.1   smtp_connect_timeout 30   router_id **lb02**} vrrp_instance VI_1 {    state **BACKUP**    interface **eth1**    virtual_router_id **55**    priority **100**    advert_int 1    authentication {        auth_type PASS        auth_pass **123456**    }    virtual_ipaddress {        **192.168.31.5 dev eth1 label eth1:1**    }}...... |

​    注解：修改配置文件主要就是上面加粗的几个地方，下面说明一下那几个参数的意思：

router_id 是路由标识，在一个局域网里面应该是唯一的；vrrp_instance VI_1{...}这是一个VRRP实例，里面定义了keepalived的主备状态、接口、优先级、认证和IP信息；state 定义了VRRP的角色，interface定义使用的接口，这里我的服务器用的网卡都是eth1,根据实际来填写，virtual_router_id是虚拟路由ID标识，一组的keepalived配置中主备都是设置一致，priority是优先级，数字越大，优先级越大，auth_type是认证方式，auth_pass是认证的密码。 virtual_ipaddress ｛...｝定义虚拟IP地址，可以配置多个IP地址，这里我定义为192.168.31.5，绑定了eth1的网络接口，虚拟接口eth1:1.

​    修改好主节点之后，保存退出，然后启动keepalived，几分钟内会生成一个虚拟IP：192.168.31.5