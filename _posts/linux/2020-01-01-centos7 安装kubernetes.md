---
layout: post
title: kubernetes安装
categories: [linux,kubernetes,k8s,docker]
description: kubernetes安装
keywords: linux,kubernetes,k8s,docker
---

kubernetes使用

# centos7 安装kubernetes

## 安装centos7
### centos7 静态ip配置
vi /etc/sysconfig/network-scripts/ifcfg-ens33
以下是可能变化的值
BOOTPROTO=static
ONBOOT=yes
以下是要增加
IPADDR=192.168.91.100
GATEWAY=192.168.91.2
DNS1=192.168.91.2

### 域名解析
vi /etc/hosts
192.168.80.33 k8s-master
192.168.80.34 k8s-node1
192.168.80.35 k8s-node2
### 修改主机名
hostnamectl set-hostname k8s-master
hostnamectl set-hostname k8s-node1
hostnamectl set-hostname k8s-node2

### centos7的一些设置

查看端口占用
ss -tnl
关闭防火墙
systemctl stop firewalld
systemctl disable firewalld
关闭selinux
vim /etc/selinux/config
SELINUX=disabled
k8s要求节点关闭 swap 禁用缓存
swapoff -a
vim /etc/fstab 将文件中和swap相关的行删除
/dev/mapper/centos-swap swap                    swap    defaults        0 0 # 此行删除

## 指定k8s和docker的镜像仓库地址
### 指定docker-ce安装仓库
cd /etc/yum.repos.d/
wget  https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

### 手动创建k8s仓库文件  
vi /etc/yum.repos.d/kubernetes.repo
[kubenetes]
name=Kubenetes Repo
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
enabled=1

### 查看镜像仓库是否有效
yum repolist

修改docker配置文件
vi /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn"
  ],
 "exec-opts": ["native.cgroupdriver=systemd"],
      "log-driver": "json-file",
      "log-opts": {
        "max-size": "100m"
      },
      "storage-driver": "overlay2",
      "storage-opts": [
        "overlay2.override_kernel_check=true"
      ]
}
启动docker服务
systemctl daemon-reload && systemctl restart docker && systemctl enable docker && systemctl status docker

## 安装kubernetes 
安装docker组件 yum install -y docker-ce 
安装k8s组件 yum -y install kubelet-1.17.2  kubeadm-1.17.2 kubectl-1.17.2


### 查看程序的安装
rpm -ql kubelet

### 修改对应参数与下面一致,多的增加,少的删除
vi /var/lib/kubelet/kubeadm-flags.env # 删除 --network-plugin=cni
KUBELET_KUBEADM_ARGS="--cgroup-driver=systemd --pod-infra-container-image=k8s.gcr.io/pause:3.1"

vi /etc/sysconfig/kubelet  #添加后面的参数
KUBELET_EXTRA_ARGS="--fail-swap-on=false --max-pods=300"

## 开机自启程序
systemctl restart kubelet && systemctl enable docker

## 给文件设置1
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables

## 查看k8s需要的镜像,此处列出的镜像可提前下载
 kubeadm config images list 
 
### python脚本批量下载所需镜像

```python
#! /usr/bin/python3
import os
images=[
"kube-apiserver:v1.17.2",
"kube-controller-manager:v1.17.2",
"kube-scheduler:v1.17.2",
"kube-proxy:v1.17.2",
"pause:3.1",
"etcd:3.4.3-0",
"coredns:1.6.5",
]
for i in images:
    pullCMD = "docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/{}".format(i)
    print("run cmd '{}', please wait ...".format(pullCMD))
    os.system(pullCMD)
    tagCMD = "docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/{} k8s.gcr.io/{}".format(i, i)
    print("run cmd '{}', please wait ...".format(tagCMD ))
    os.system(tagCMD)
    rmiCMD = "docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/{}".format(i)
    print("run cmd '{}', please wait ...".format(rmiCMD ))
    os.system(rmiCMD)
```
### 下载的镜像重新打符合kubeadm config images list 的标签tag
docker tag k8s.gcr.io/kube-apiserver:v1.17.2 k8s.gcr.io/kube-apiserver:v1.17.5
docker tag k8s.gcr.io/kube-controller-manager:v1.17.2 k8s.gcr.io/kube-controller-manager:v1.17.5
docker tag k8s.gcr.io/kube-scheduler:v1.17.2 k8s.gcr.io/kube-scheduler:v1.17.5
docker tag k8s.gcr.io/kube-proxy:v1.17.2 k8s.gcr.io/kube-proxy:v1.17.5

 
### k8s初始化帮助
 kubeadm init --help

### 添加参数
 vi /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
Environment="KUBELET_CGROUP_ARGS=--cgroup-driver=systemd"
 
### 重启kubelet
systemctl daemon-reload && systemctl restart kubelet &&  systemctl status kubelet

### 初始化k8s ,指定pod网段,服务网段
kubeadm init --kubernetes-version=v1.17.2 --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12  --ignore-preflight-errors=Swap 
 
### 有需要的时候执行重新初始化k8s
kubeadm reset


## 成功安装kubernetes环境	
```shell
	Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:
# 复制配置文件
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:
# 使用下面的语句添加节点到集群
kubeadm join 192.168.80.33:6443 --token yg8hz5.53lv8kuf8zbvq1ly \
    --discovery-token-ca-cert-hash sha256:d0680112db3939b99219218e62cb0385b764545b252590cdc94a7b2d3d45e306
```



## 主节点不能使用的问题,执行如下命令
kubectl taint nodes --all node.kubernetes.io/not-ready-

