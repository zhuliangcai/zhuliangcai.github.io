---
layout: post
title: kubernetes使用
categories: [linux,kubernetes,k8s,docker]
description: kubernetes使用
keywords: linux,kubernetes,k8s,docker
---

kubernetes使用

## 安装kubernetes

参考：2020-01-01-centos7 安装kubernetes.md

https://www.jianshu.com/p/99d09406373e

# kubernetes

kubectl --help

## 查看资源使用情况 
查看各个节点的内存cpu使用
kubectl -n ns-retail-dev top nodes
查看各个pod的内存使用
kubectl -n ns-retail-dev top pods
查看单个pod的内存使用
kubectl -n ns-retail-dev top pods pod-name
查看容器数据流
docker stats 9aa1446a66ca
## 获取命名空间
kubectl get ns
## 获取nodes
kubectl get nodes
## 获取pods
kubectl get pods 默认命名空间
kubectl get pods -A  所有命名空间下的pods
kubectl get service -A  所有命名空间下的pods
kubectl get rc -A  所有命名空间下的pods
  kubectl get replicasets -A   显示有关ReplicaSet 对象的信息
## 获取指定命名空间下的pods
kubectl get pods -ns system-test -o wide/yaml/json
## 获取服务
kubectl get svc/service
kubectl get svc/ngx-svc -o yaml

获取指定命名空间下的容器组pod信息 -o 输出格式  
kubectl get -n ns-retail-dev  pod/v7-scm-746c849465-fmh8h -o json 
根据短语获取特定值
kubectl get -n ns-retail-dev  pod/v7-scm-746c849465-fmh8h -o template --template={{.status.hostIP}} 

### List all replication controllers and services together in ps output format. 
  kubectl get rc,services
  kubectl get rc,service,pods -o wide -n ns-retail-dev  查看指定命名空间下更多的 服务或pods

### List one or more resources by their type and names.
  kubectl get rc/web service/frontend pods/web-pod-13je7

## describe查看信息
 查看服务信息，
 kubectl describe node 172.20.176.190
 查看节点信息，
 kubectl describe svc/ngx-dep
 查看指定命名空间下的容器组pod信息，
 kubectl describe pod v7-scm-746c849465-fmh8h -n ns-retail-dev
 查看指定service的信息
  kubectl describe service kubernetes
 查看默认[指定命名空间]下的所有[指定]pod信息
 kubectl describe pod [pod-name] [-n ns]

## 进入指定命名空间下的指定pods的第一个容器
如果有多个容器，则使用 -c 容器名 选项
kubectl exec -n namespace-name -it pod-name  /bin/bash
[root@pod-name /]#ps aux  查看容器中的进程，容器中只运行指定的进程，非常简洁

## 查看docker的镜像仓库

docker info  最后会显示 registry

# 创建命令
创建命名空间
kubectl create ns yournamespace


kubectl create service clusterip ngx-svc --tcp=80:80 



kubectl delete svc/ngx-svc

kubectl create service clusterip ngx-dep --tcp=80:80 

kubectl expose deployment hello-world --type=LoadBalancer --name=my-services

# 获取资源配置清单信息
## 1.获取api-version资源信息
kubectl  api-versions
## 获取yaml文件编写需要的内容
kubectl  explain  [资源名字]
## 查看创建pod需要的信息
kubectl explain pods
## 查看pod中spec需要的信息
kubectl explain pods.spec
kubectl explain pods.spec.container.lifecycle



# 如何在Kubernetes里创建一个Nginx应用

拉取镜像
 docker pull nginx
给镜像打标签
 docker tag nginx nginx:v1
单独拉取镜像不太好用，最好是kubernetes自动拉取镜像

1. k8s创建命名空间
kubectl create ns-test

2. 在指定的命名空间下创建nginx-demo应用 
 kubectl run --image=nginx nginx-demo -n ns-test --port=80 
3. 查看pods
[root@v-jdy-k8s01 ~]# kubectl get pods  -n ns-test
NAME                          READY   STATUS    RESTARTS   AGE
nginx-demo-7d588546bf-zj79q   1/1     Running   0          10m
4. 查看创建过程
kubectl describe pod nginx-demo-7d588546bf-zj79q -n ns-test
创建过程，提升在哪个node中创建，在做哪些步骤
Events:
  Type    Reason     Age    From                    Message
  ----    ------     ----   ----                    -------
  Normal  Scheduled  8m28s  default-scheduler       Successfully assigned ns-test/nginx-demo-7d588546bf-zj79q to 172.20.182.35
  Normal  Pulling    8m26s  kubelet, 172.20.182.35  Pulling image "nginx"
  Normal  Pulled     68s    kubelet, 172.20.182.35  Successfully pulled image "nginx"
  Normal  Created    68s    kubelet, 172.20.182.35  Created container nginx-demo
  Normal  Started    67s    kubelet, 172.20.182.35  Started container nginx-demo

5. 查看pods明细信息
 kubectl describe pods -n ns-test

6. 查看pod的ip
 [root@v-jdy-k8s01 ~]# kubectl get pods -n ns-test -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP            NODE            NOMINATED NODE   READINESS GATES
nginx-demo-7d588546bf-zj79q   1/1     Running   0          13m   172.30.88.7   172.20.182.35   <none>           <none>
7. 访问
[root@v-jdy-k8s01 ~]# curl 172.30.88.7
```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```



8. 查看创建的部署
kubectl get deployment -n ns-test
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-demo   0/1     1            0           2m44s


9. 发布给外部
kubectl expose deployment nginx-demo --name=nginx-service --type=NodePort -n ns-test

10. 查看服务
[root@v-jdy-k8s01 ~]# kubectl get svc -n ns-test
NAME            TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
nginx-service   NodePort   10.254.203.172   <none>        80:33360/TCP   31s

用json格式展示
 kc get svc nginx-service -o json -n ns-test
```json
 "ports": [
            {
                "nodePort": 33360, 节点ip对应的端口
                "port": 80,  集群ip对应的端口
                "protocol": "TCP",
                "targetPort": 80 容器ip对应的端口
            }

```
外部访问：
http://172.20.182.35:33360/
集群中访问
[root@v-jdy-k8s01 ~]# curl 10.254.203.172:80


11. 进入nginx容器
kubectl exec -n ns-test -it nginx-demo-7d588546bf-zj79q  /bin/bash
从容器中考出文件
kubectl cp nginx-demo-7d588546bf-zj79q:/usr/share/nginx/html/index.html index.html -n ns-test
拷贝文件到容器中
kubectl cp index.html nginx-demo-7d588546bf-zj79q:/usr/share/nginx/html/index.html  -n ns-test


12. 创建tomcat并配置反向代理

创建tomcat
 kubectl run --image=library/tomcat tomcat8 -n ns-test --port=8080
 查看tomcat的部署情况
kubectl describe pods tomcat8-6bc9dfbc6c-w8ldt -n ns-test
查看ip
 kubectl get pods -n ns-test -o wide
 发布给外部使用
kubectl expose deployment tomcat8 --name=tomcat8-service --type=NodePort -n ns-test
 查看服务
 kubectl get svc -n ns-test

kubectl exec -n ns-test -it tomcat8-6bc9dfbc6c-w8ldt  /bin/bash

kubectl cp nginx-demo-7d588546bf-zj79q:/etc/nginx/nginx.conf nginx.conf -n ns-test

kubectl cp  nginx.conf nginx-demo-7d588546bf-zj79q:/etc/nginx/nginx.conf -n ns-test
nginx反向代理配置
```conf

server {
        listen       80;
        server_name  localhost;

        location /abc {
            proxy_pass http://10.254.12.51:8080;
            index  index.html index.htm index.jsp;
        }
    }

```
13. 编辑一个在线资源
    
kubectl edit deployment/nginx-demo -o yaml -n ns-test

14. 扩容/缩容 
    只需改变replicas的值即可达到目的
kc scale --replicas=3 deploy/nginx-demo -n ns-test

15. 获取ingress,路由总线
 kubectl get ingresses -n ns-retail-dev

16.      根据pod名称删除
kubectl delete deployment nginx-demo(NAME) -n ns-test

master:
	apiserver: 使用kubectl restapi webui
	etcd
	controller-manager
	scheduler
	
node:
	kubelet: 和 apiserver通信,
	kube-proxy: 创建虚拟网卡
	docker-container : 容器程序
	
Pod : 调度的最小单位
deployment: 维持pod的数量
kubectl edit deployments d1 修改对应的配置文件

service: 将多个Pod服务对外提供一个共同的访问,做负载均衡

创建服务
kubectl expose deployment d1 --target-port 80 --type NodePort
kubectl cluster-info 查看集群信息

coredns: 集群内域名解析,将服务名和ip做映射,kubernetes集群中相互解析

ingress: 外部域名解析:外网ip->服务  用户访问->集群对外ip:port->service->pod->container : 负载均衡

Kubernetes 之上，玩转企业级容器管理平台 KubeSphere  图形化操作k8s

# k8s WEB-UI
kuboard
kubesphere

安装
https://www.bilibili.com/video/BV1nK41157em?from=search&seid=5663592372878727043
# 创建一个Master节点
kubeadm  init

# 将一个Node节点加入到当前集群中
kubeadm join <Master节点ip和端口>



# 快速进入k8s docker容器脚本
```shell

#!/bin/bash
# 快速进入k8s docker容器脚本
echo "entering k8s docker "$1

CONTAINER_ID=$(kubectl get pod -n ns-retail-master -o wide|grep v7-$1|awk '{print $1}')
kubectl exec -it ${CONTAINER_ID} -n ns-retail-master /bin/bash

#!/bin/bash
# 快速进入k8s docker容器脚本
echo "entering k8s docker "$1

CONTAINER_ID=$(kubectl get pod -n ns-retail-dev -o wide|grep v7-$1|awk '{print $1}')
kubectl exec -it ${CONTAINER_ID} -n ns-retail-dev /bin/bash

#!/bin/bash
# 快速进入k8s docker容器脚本
echo "entering k8s docker "$1

CONTAINER_ID=$(kubectl get pod -n ns-retail-feature1 -o wide|grep v7-$1|awk '{print $1}'|head -n 1)
kubectl exec -it ${CONTAINER_ID} -n ns-retail-feature1 /bin/bash


```


# Harbor
版本 v1.8.0-25bb24ca
Harbor是一个用于存储和分发Docker镜像的企业级Registry服务器，通过添加一些企业必需的功能特性，例如安全、标识和管理等，扩展了开源Docker Distribution。作为一个企业级私有Registry服务器，Harbor提供了更好的性能和安全。提升用户使用Registry构建和运行环境传输镜像的效率。

开源/第三方许可协议

默认用户名密码
admin/Harbor12345

docker配置私有仓库的位置
[root@vlocalhos portman]# docker login reg.xxx.com
Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[root@vlocalhos portman]# cat /root/.docker/config.json


# docker 推送镜像到私有仓库
登录
docker login reg.jdy.com
打标签 私有仓库地址/项目名称/镜像名:标签号
docker tag nginx:v1 reg.jdy.com/sentinel/nginx:v1
推送镜像
docker push reg.jdy.com/sentinel/nginx:v1
删除本地镜像
docker rmi reg.jdy.com/sentinel/nginx:v1
拉取私有仓库镜像
docker pull reg.jdy.com/sentinel/nginx:v1
查看镜像
docker images|grep nginx
## kubectl get 各种资源

```shell

[root@v-jdy-k8s01 ~]# kubectl get
alertmanagers.monitoring.coreos.com                           nodes.metrics.k8s.io
apiservices.apiregistration.k8s.io                            persistentvolumeclaims
auditsinks.auditregistration.k8s.io                           persistentvolumes
certificatesigningrequests.certificates.k8s.io                poddisruptionbudgets.policy
clusterrolebindings.rbac.authorization.k8s.io                 podmonitors.monitoring.coreos.com
clusterroles.rbac.authorization.k8s.io                        podpresets.settings.k8s.io
componentstatuses                                             pods
configmaps                                                    podsecuritypolicies.extensions
controllerrevisions.apps                                      podsecuritypolicies.policy
cronjobs.batch                                                pods.metrics.k8s.io
cronworkflows.argoproj.io                                     podtemplates
csidrivers.storage.k8s.io                                     priorityclasses.scheduling.k8s.io
csinodes.storage.k8s.io                                       prometheuses.monitoring.coreos.com
customresourcedefinitions.apiextensions.k8s.io                prometheusrules.monitoring.coreos.com
daemonsets.apps                                               replicasets.apps
daemonsets.extensions                                         replicasets.extensions
deployments.apps                                              replicationcontrollers
deployments.extensions                                        resourcequotas
endpoints                                                     rolebindings.rbac.authorization.k8s.io
events                                                        roles.rbac.authorization.k8s.io
events.events.k8s.io                                          runtimeclasses.node.k8s.io
horizontalpodautoscalers.autoscaling                          secrets
ingresses.extensions                                          serviceaccounts
ingresses.networking.k8s.io                                   servicemonitors.monitoring.coreos.com
jobs.batch                                                    services
leases.coordination.k8s.io                                    statefulsets.apps
limitranges                                                   storageclasses.storage.k8s.io
mutatingwebhookconfigurations.admissionregistration.k8s.io    validatingwebhookconfigurations.admissionregistration.k8s.io
namespaces                                                    volumeattachments.storage.k8s.io
networkpolicies.extensions                                    workflows.argoproj.io
networkpolicies.networking.k8s.io                             workflowtemplates.argoproj.io
nodes
[root@v-jdy-k8s01 ~]# kubectl get

创建

kubectl create -f xxx.yaml

查询

kubectl get pod yourPodName

kubectl describe pod yourPodName

删除

kubectl delete pod yourPodName

更新

kubectl replace /path/to/yourNewYaml.yaml

```


## 参考：
https://www.cnblogs.com/tianleblog/p/11935056.html
https://www.cnblogs.com/zhangb8042/p/9572701.html
kubernetes核心概念总结
https://www.cnblogs.com/zhenyuyaodidiao/p/6500720.html
