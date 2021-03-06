---
layout: post
title: zookeeper相关自动化脚本
categories: [linux,shell,自动化,脚本]
description:  zookeeper相关自动化脚本
keywords: linux,shell,自动化脚本
---

自动化脚本,省去重复的烦恼

## 单机版zookeeper实例并运行

```shell
#!/bin/bash
<<!
 **********************************************************
 * Author        : 朱良才
 * Email         : 1024955966@qq.com
 * Last modified : 2016-01-13 00:20
 * Filename      : z.singleton.zookeeper.sh
 * Description   :
 * *******************************************************
!
#默认安装zookeeper-3.4.6.tar.gz 脚本
#创建单机版 zookeeper实例并运行
###############################
#以下是手动配置项
###############################
zoofiletar='zookeeper-3.4.6.tar.gz'
zoodir='zookeeper-3.4.6'
singlezoo='zookeeper-3.4.6.singleton'
#如果文件夹存在则不解压文件zookeeper-3.4.6.tar.gz
if [ ! -x $zoodir ]; then 
   if [ $zoofiletar ];then
      tar zxf $zoofiletar 
   else
   	 echo "you should give a filename like zookeeper-x.x.x.tar.gz" 
   fi
else
   echo "$zoodir already exists!"
fi

#改名
mv $zoodir $singlezoo

cd $singlezoo
zoopath=`pwd`
mkdir $zoopath/data
datadir="dataDir=${zoopath}/data"
olddir=`grep "dataDir=" $zoopath/conf/zoo_sample.cfg`
#echo "$olddir $datadir"
myolddir=`echo $olddir | sed "s/\//\\\//g"`
#echo "$myolddir"
mydatadir=`echo $datadir | sed "s/\//\\\//g"`

#获取dataDir=所在的行号
num=`grep -n "dataDir=" $zoopath/conf/zoo_sample.cfg | cut -d':' -f1`
#删除行 把内容存入临时文件
sed "${num}d" $zoopath/conf/zoo_sample.cfg > $zoopath/conf/zoo.tmp.cfg

# sed替换命令 a ∶ 新增， a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)
echo $mydatadir
# 在just出现的位置的下一行添加 $mydatadir

sed /just/a\\$mydatadir $zoopath/conf/zoo.tmp.cfg > $zoopath/conf/zoo.cfg
echo "zookeeper is install ok!"

path=`pwd`
echo $path
./bin/zkServer.sh start
./bin/zkServer.sh status

#zoofiletar=`ls -al|grep "^-.*zookeeper.*\.tar\.gz" | cut -d' ' -f 11`
```

## 集群启动脚本

start-cluster-better.sh

```shell
#!/bin/bash
myecho(){
	echo "================= $1  ================="
}

startzoo(){
	myecho "正在启动zookeeper"
	for i in centos@hd3 centos@hd4 centos@hd5
	do
		ssh $i '/opt/zookeeper/bin/zkServer.sh start'
	done
}
startstorm(){
	
	for i in centos@hd3 centos@hd4 centos@hd5
	do
		myecho "正在后台启动 $i storm nimbus "
		ssh $i 'storm nimbus 1>/dev/null 2>&1 &'
	done

	for i in centos@hd3 centos@hd4 centos@hd5
	do
		myecho "正在后台启动 $i storm supervisor "
		ssh $i 'storm supervisor 1>/dev/null 2>&1 &'
	done
}


starthdfs(){
	myecho "正在启动HDFS"
	ssh centos@hd3 '/opt/hadoop/sbin/start-dfs.sh'
}
startyarn(){
	myecho "正在启动YARN"
	ssh centos@hd3 '/opt/hadoop/sbin/start-yarn.sh'
}
startjobhistory(){
	myecho "正在启动jobhistoryserver"
	ssh centos@hd3 '/opt/hadoop/sbin/hadoop-daemon.sh start historyserver'
}

startall(){
	myecho "开启启动所有节点服务"
	startzoo
	starthdfs
	startyarn
}

choseOne(){
	echo "$1"
	case "$1" in
			"zookeeper")					
					startzoo
					#输出两个分号
					;;
			"storm")					
					startstorm
					#输出两个分号
					;;
			"hdfs")	
					starthdfs
					;;
			"yarn")
					startyarn
					;;
			"historyserver")
					startjobhistory
					;;
			"all")
					startall
					;;
			*)
					#其它输入
					echo "Usage: $0 {zookeeper|storm|hdfs|yarn|historyserver|all}"
					;;
	esac


}

# 执行入口

choseOne $1

# if [ $# -eq 1 ];
# then
# 	choseOne $1
# else
# 	startall 
# fi
```

### 搭建zookeeper集群思路

z.cluster.zookeeper.sh的使用方法

在linux上新建一个目录例如zoos,上传z.cluster.zookeeper.sh脚本和zookeeper-3.4.6.tar.gz文件到这个目录中,如果脚本能直接运行则运行,否则使用命令chmod u+x z.cluster.zookeeper.sh 授予执行权限再运行,搭建出一个伪集群


真实集群脚本创建思路分析

1.配置好linux系统之间的免密登录      成功
2.创建单个zookeeper并修改zookeeper集群配置  成功
3.分发zookeeper到各个节点        成功
4.远程启动各个zookeeper节点实例  暂时测试不成功

实现脚本true.cluster.zookeeper.sh


集群扩容,在原有3个节点的集群基础上扩容2个节点

思路分析
1. 新配置2个节点
2. 分发到新机器上,依次启动
3. 修改原来的节点配置,依次启动,扩容成功

创建新节点副本脚本create.new.node.sh

集群收缩 ,在原有5个节点的集群基础上减少2个节点
修改保留节点的配置后依次重启，重启完成后依次关闭2个不需要的节点即可。


## zookeeper集群启动脚本

```shell
#!/bin/bash

zoofun(){
	ssh centos@hd3 "/opt/zookeeper/bin/zkServer.sh $1"
	ssh centos@hd4 "/opt/zookeeper/bin/zkServer.sh $1"
	ssh centos@hd5 "/opt/zookeeper/bin/zkServer.sh $1"
}


ARR=("start" "stop" "restart" "status")
if echo "${ARR[@]}" | grep -w "$1" &>/dev/null; then
    # 执行调用远程脚本
	zoofun $1
else
	echo "Usage: $0 {start|stop|restart|status}"
fi

```

## zookeeper自动创建伪集群脚本

```shell
#!/bin/bash
<<!
 **********************************************************
 * Author        : 朱良才
 * Email         : 1024955966@qq.com
 * Last modified : 2016-01-13 00:20
 * Filename      : z.cluster.zookeeper.sh
 * Description   :
 * *******************************************************
!
#默认安装zookeeper-3.4.6.tar.gz 脚本 
#创建伪分布式 zookeeper集群
###############################
#以下是手动配置项
###############################

hostip='192.168.25.135'
zoofiletar='zookeeper-3.4.6.tar.gz'
zoodir='zookeeper-3.4.6'

###############################

#如果文件夹存在则不解压文件zookeeper-3.4.6.tar.gz
if [ ! -x $zoodir ]; then 
   if [ $zoofiletar ];then
      tar zxf $zoofiletar 
   else
   	 echo "you should give a filename like zookeeper-x.x.x.tar.gz" 
   fi
else
   echo "$zoodir already exists!"
fi


zt="czookeeper"

thispath=`pwd`
echo $thispath

#创建文件的函数
createFile(){
	#如果文件存在则删除文件
	if [ -f $1 ];then
		rm -f $1
	fi
	cat >> $1 <<EOF
#!/bin/bash
EOF
	#添加执行权限
	chmod +x $1
}
#启动伪集群脚本
startzoos="$thispath/start.zookeepers.sh" 
createFile $startzoos
#关闭伪集群脚本
stopzoos="$thispath/stop.zookeepers.sh"
createFile $stopzoos 
#查看伪集群状态脚本
statuszoos="$thispath/status.zookeepers.sh"
createFile $statuszoos 

#配置文件数组，用于添加server
myzoopaths=()
#echo $tomhome
#遍历
for N in {1..3}
do
	zoo="${zt}${N}"
	cp -r $zoodir $zoo
	cd $zoo
	zoopath=`pwd`
	echo "${zoopath}/bin/zkServer.sh start" >> $startzoos
	echo "${zoopath}/bin/zkServer.sh stop" >> $stopzoos
	echo "${zoopath}/bin/zkServer.sh status" >> $statuszoos
	mkdir $zoopath/data
	datadir="dataDir=${zoopath}/data"
	olddir=`grep "dataDir=" $zoopath/conf/zoo_sample.cfg`
	#echo "$olddir $datadir"
	myolddir=`echo $olddir | sed "s/\//\\\//g"`
	#echo "$myolddir"
	mydatadir=`echo $datadir | sed "s/\//\\\//g"`
	#echo "$mydatadir"
	#cp $zoopath/conf/zoo_sample.cfg $zoopath/conf/zoo.cfg
	#获取dataDir=所在的行号
	num=`grep -n "dataDir=" $zoopath/conf/zoo_sample.cfg | cut -d':' -f1`
	sed -e "s/2181/228${N}/g" -e "${num}d" $zoopath/conf/zoo_sample.cfg > $zoopath/conf/zoo.tmp.cfg
	#echo $mydatadir
	#在指定字符串的后面添加行
	sed /just/a\\$mydatadir $zoopath/conf/zoo.tmp.cfg > $zoopath/conf/zoo.cfg	
	
	myzoopaths["${N}"]=$zoopath
	echo "$zoo is install ok!"
	#touch $datadir/myid
	echo "${N}" > $zoopath/data/myid
	
	cd ..
done

for a in ${myzoopaths[*]}
do
	for N in {1..3}
	do
		echo "server.${N}=${hostip}:288${N}:388${N}" >> $a/conf/zoo.cfg
	done
done
rm -rf $zoodir

###############################
#zoofiletar=`ls -al|grep "^-.*zookeeper.*\.tar\.gz" | cut -d" " -f 9`
#获取解压后的zookeeper文件夹的名字
#zoodir=`ls -al | grep "^d.*zookeeper.*$" |cut -d" " -f 14`
#zoodir='zookeeper-3.4.6'
###############################
#启动伪集群
$startzoos
#$stopzoos
#查看伪集群状态
$statuszoos
```
## zookeeper自动化多实例集群创建脚本

创建真分布式 zookeeper集群 create.new.node.sh
```shell
#!/bin/bash
<<!
 **********************************************************
 * Author        : 朱良才
 * Email         : 1024955966@qq.com
 * Last modified : 2016-01-13 00:20
 * Filename      : z.cluster.zookeeper.sh
 * Description   :
 * *******************************************************
!
#默认安装zookeeper-3.4.6.tar.gz 脚本 
#创建真分布式 zookeeper集群
###############################
#以下是手动配置项
###############################
#所有节点IP
ALLIP=("192.168.25.164" "192.168.25.165" "192.168.25.166" "192.168.25.162" "192.168.25.163")
echo 
zoofiletar='zookeeper-3.4.6.tar.gz'
zoodir='zookeeper-3.4.6'

###############################

#如果文件夹存在则不解压文件zookeeper-3.4.6.tar.gz
if [ ! -x $zoodir ]; then 
   if [ $zoofiletar ];then
      tar zxf $zoofiletar 
   else
   	 echo "you should give a filename like zookeeper-x.x.x.tar.gz" 
   fi
else
   echo "$zoodir already exists!"
   rm -rf $zoodir
   tar zxf $zoofiletar
fi


# tar & install & scp
mkdir $zoodir/data
datadir="dataDir=/opt/${zoodir}/data"

#在指定字符串的后面添加行

num=`grep -n "dataDir=" $zoodir/conf/zoo_sample.cfg | cut -d':' -f1`
sed  -e "${num}d" $zoodir/conf/zoo_sample.cfg > $zoodir/conf/zoo.tmp.cfg
sed /just/a\\$datadir $zoodir/conf/zoo.tmp.cfg > $zoodir/conf/zoo.cfg

echo "$zoofiletar is install ok!"
#touch $datadir/myid


# for insert
for N in {1..5}
do
	echo "server.${N}=${ALLIP[$[${N}-1]]}:288${N}:388${N}" >> $zoodir/conf/zoo.cfg
done

echo "新节点配置完成,创建myid并分发即可"


###############################

```

## zookeeper自动化多节点集群创建脚本

```shell
#!/bin/bash
<<!
 **********************************************************
 * Author        : 朱良才
 * Email         : 1024955966@qq.com
 * Last modified : 2016-01-13 00:20
 * Filename      : z.cluster.zookeeper.sh
 * Description   :
 * *******************************************************
!
#默认安装zookeeper-3.4.6.tar.gz 脚本 
#创建真分布式 zookeeper集群
###############################
#以下是手动配置项
###############################
#所有节点IP
ALLIP=("192.168.25.100" "192.168.25.110" "192.168.25.120")
echo 
zoofiletar='zookeeper-3.4.6.tar.gz'
zoodir='zookeeper-3.4.6'

###############################

#如果文件夹存在则不解压文件zookeeper-3.4.6.tar.gz
if [ ! -x $zoodir ]; then 
   if [ $zoofiletar ];then
      tar zxf $zoofiletar 
   else
   	 echo "you should give a filename like zookeeper-x.x.x.tar.gz" 
   fi
else
   echo "$zoodir already exists!"
   rm -rf $zoodir
   tar zxf $zoofiletar
fi


# tar & install & scp
mkdir $zoodir/data
datadir="dataDir=/export/servers/${zoodir}/data"
#olddir=`grep "dataDir=" $zoodir/conf/zoo_sample.cfg`
#echo "$olddir $datadir"
#myolddir=`echo $olddir | sed "s/\//\\\//g"`
#echo "$myolddir"
#mydatadir=`echo $datadir | sed "s/\//\\\//g"`
#echo "$mydatadir"
#cp $zoopath/conf/zoo_sample.cfg $zoopath/conf/zoo.cfg
#获取dataDir=所在的行号
#sed -i 's/abc/xxx/g' file
#
#abc修改前的字符串
#xxx是修改后的字符串
#file是要被修改的文件
#sed "s/原字符串包含/替换字符串包含/" 
##可以使用 # 作为分隔符，此时中间出现的 / 不会作为分隔符
#在指定字符串的后面添加行
#sed '行号c 新的内容' 要处理的文件
#num=`grep -n "dataDir=" $zoodir/conf/zoo_sample.cfg | cut -d':' -f1`
#sed '${num}c ${mydatadir}'  $zoodir/conf/zoo_sample.cfg > $zoodir/conf/zoo.cfg
#sed -i 's/${myolddir}/${mydatadir}/g'  $zoodir/conf/zoo_sample.cfg  > $zoodir/conf/zoo.cfg
num=`grep -n "dataDir=" $zoodir/conf/zoo_sample.cfg | cut -d':' -f1`
sed  -e "${num}d" $zoodir/conf/zoo_sample.cfg > $zoodir/conf/zoo.tmp.cfg
sed /just/a\\$datadir $zoodir/conf/zoo.tmp.cfg > $zoodir/conf/zoo.cfg

echo "$zoofiletar is install ok!"
#touch $datadir/myid


# for insert
for N in {1..3}
do
	echo "server.${N}=${ALLIP[$[${N}-1]]}:288${N}:388${N}" >> $zoodir/conf/zoo.cfg
done


#分发到各台机器
for N in {1..3}
do
	echo ${N} > $zoodir/data/myid
	scp -r $zoodir root@${ALLIP[$[${N}-1]]}:/export/servers/ > /dev/null
	echo "发送副本到机器${ALLIP[$[${N}-1]]}成功"
done 
#移除不需要的副本
rm -rf $zoodir
#创建集群启动脚本
###############################
#创建文件的函数
createFile(){
	#如果文件存在则删除文件
	if [ -f $1 ];then
		rm -f $1
	fi
	cat >> $1 <<EOF
#!/bin/bash
EOF
	#添加执行权限
	chmod +x $1
}
#启动伪集群脚本
startzoos="start.cluster.zookeepers.sh" 
createFile $startzoos
for N in {1..3}
do
	#echo "ssh root@${ALLIP[$[${N}-1]]} '/export/servers/zookeeper-3.4.6/bin/zkServer.sh start'" >> $startzoos
	echo "ssh0$[${N}+3]" >> $startzoos
	echo "/export/servers/zookeeper-3.4.6/bin/zkServer.sh start" >> $startzoos
	echo "exit" >> $startzoos
done 

echo "执行启动脚本$startzoos,可启动集群了"


###############################

```


