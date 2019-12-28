---
layout: post
title: pip install指定国内源镜像
categories: [python,pip]
description: pip install指定国内源镜像
keywords: python,pip
---

pip install指定国内源镜像



## linux下的pip安装

wget https://bootstrap.pypa.io/get-pip.py

sudo python get-pip.py

修改源方法：

### 使用国内镜像源 
临时使用： 
可以在使用pip的时候在后面加上-i参数，指定pip源 
eg: pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple

永久修改： 
linux: 
修改 ~/.pip/pip.conf (没有就创建一个)， 内容如下：

[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
windows: 
直接在user目录中创建一个pip目录，如：C:\Users\xx\pip，新建文件pip.ini，内容如下

[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple


## windows的python安装包默认带了pip

python pip install指定国内源镜像
　　有时候安装一些依赖包，网不好，直接超时，或者这个包就是死都下不下来的时候，可以指定国内源镜像。

　　pip install -i 国内镜像地址 包名

　　e.g. pip install -i  http://mirrors.aliyun.com/pypi/simple/ numpy 这是临时指定镜像地址

清华：https://pypi.tuna.tsinghua.edu.cn/simple

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/ 

豆瓣：http://pypi.douban.com/simple/

note：新版ubuntu要求使用https源，要注意。

部分信息转自：https://www.cnblogs.com/wqpkita/p/7248525.html

## 设置镜像源
https://blog.csdn.net/wls666/article/details/95456309

### 方法一：Windows下永久更换镜像源
在windows文件管理器中输入“ %APPDATA% ”，如下图所示：

![](https://img-blog.csdnimg.cn/2019071111371594.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dsczY2Ng==,size_16,color_FFFFFF,t_70)

3在新建的 pip.ini 文件中输入以下内容，然后保存。
注意:" index-url " 的内容是镜像源的路径，可以更换
```ini
[global]
timeout = 6000
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com

```
**测试有效**

————————————————
版权声明：本文为CSDN博主「oito」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/wls666/article/details/95456309