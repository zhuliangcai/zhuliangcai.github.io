---
layout: post
title: 深入理解Maven中的Profile
categories: [java,maven,profile]
description: 深入理解Maven中的Profile
keywords: java,maven,profile
---

深入理解Maven中的Profile

## profile简介
　　profile可以让我们定义一系列的配置信息，然后指定其激活条件。这样我们就可以定义多个profile，然后每个profile对应不同的激活条件和配置信息，从而达到不同环境使用不同配置信息的效果。比如说，我们可以通过profile定义在jdk1.5以上使用一套配置信息，在jdk1.5以下使用另外一套配置信息；或者有时候我们可以通过操作系统的不同来使用不同的配置信息，比如windows下是一套信息，linux下又是另外一套信息，等等。

## Profiles下面允许出现的元素
Profile能让你为一个特殊的环境自定义一个特殊的构建，profile使得不同环境间构建的可移植性成为可能。Maven中的profile是一组可选的配置，可以用来设置或者覆盖配置默认值。有了profile，你就可以为不同的环境定制构建。profile可以在pom.xml中配置，并给定一个id。然后你就可以在运行Maven的时候使用的命令行标记告诉Maven运行特定profile中的目标。一个Profiles下面允许出现的元素如下：

```xml
<project>
    <profiles>
        <profile>
            <build>
                <defaultGoal>...</defaultGoal>
                <finalName>...</finalName>
                <resources>...</resources>
                <testResources>...</testResources>
                <plugins>...</plugins>
            </build>
            <reporting>...</reporting>
            <modules>...</modules>
            <dependencies>...</dependencies>
            <dependencyManagement>...</dependencyManagement>
            <distributionManagement>...</distributionManagement>
            <repositories>...</repositories>
            <pluginRepositories>...</pluginRepositories>
            <properties>...</properties>
        </profile>
    </profiles>
</project>                        
```
　　一个Profile可以覆盖项目构件的最终名称，项目依赖，插件配置以影响构建行为，Profile还可以覆盖分发配置。maven提供了一种针对不同环境参数`激活`一个profile的方式，这就叫做profile激活。

## profile的定义位置
　　我们可以有多个地方定义profile。定义的地方不同，它的作用范围也不同。针对于特定项目的profile配置我们可以定义在该项目的pom.xml中。针对于特定用户的profile配置，我们可以在用户的settings.xml文件中定义profile。该文件在用户家目录下的`.m2`目录下。全局的profile配置。全局的profile是定义在Maven安装目录下的`conf/settings.xml`文件中的。
## profile中能定义的信息
　　profile中能够定义的配置信息跟profile所处的位置是相关的。以下就分两种情况来讨论，一种是定义在settings.xml中，另一种是定义在pom.xml中。
#### profile定义在settings.xml中

　　当profile定义在settings.xml中时意味着该profile是全局的，它会对所有项目或者某一用户的所有项目都产生作用。因为它是全局的，所以在settings.xml中只能定义一些相对而言范围宽泛一点的配置信息，比如远程仓库等。而一些比较细致一点的需要根据项目的不同来定义的就需要定义在项目的pom.xml中。具体而言，能够定义在settings.xml中的信息有`<repositories>`、`<pluginRepositories>`和`<properties>`。定义在`<properties>`里面的键值对可以在pom.xml中使用。

#### profile定义在pom.xml中

　　定义在pom.xml中的profile可以定义更多的信息。主要有以下这些：
```xml
<repositories>
<pluginRepositories>
<dependencies>
<plugins>
<properties>
<dependencyManagement>
<distributionManagement>
```
还有build元素下面的子元素，主要包括：
```xml
<defaultGoal>
<resources>
<testResources>
<finalName>
```
## profile的激活方式
　　Maven给我们提供了多种不同的profile激活方式。比如我们可以使用-P参数显示的激活一个profile，也可以根据环境条件的设置让它自动激活等。下面将对它们一一进行介绍：

#### 使用activeByDefault设置激活

```xml
<profiles> 
    <profile> 
        <id>profileTest1</id> 
        <properties> 
            <hello>world</hello> 
        </properties> 
        <activation> 
            <activeByDefault>true</activeByDefault> 
        </activation> 
    </profile> 
    <profile> 
        <id>profileTest2</id> 
        <properties> 
            <hello>andy</hello> 
        </properties> 
    </profile> 
</profiles> 
```
　　我们可以在profile中的activation元素中指定激活条件，当没有指定条件，然后指定activeByDefault为true的时候就表示当没有指定其他profile为激活状态时，该profile就默认会被激活。所以当我们调用`mvn package`的时候上面的profileTest1将会被激活，但是当我们使用`mvn package –P profileTest2`的时候将激活profileTest2，而这个时候profileTest1将不会被激活。
#### 在settings.xml中使用activeProfiles指定处于激活状态的profile

　　我们可以在settings.xml中使用activeProfiles来指定需要激活的profile，这种方式激活的profile将所有情况下都处于激活状态。比如现在我们定义了如下两个profile

```xml
<profiles> 
    <profile> 
        <id>profileTest1</id> 
        <properties> 
            <hello>world</hello> 
        </properties> 
    </profile> 
    <profile> 
        <id>profileTest2</id> 
        <properties> 
            <hello>andy</hello> 
        </properties> 
    </profile> 
</profiles> 
```
　　这里的profile可以是定义在settings.xml中的，也可以是定义在pom.xml中的。这个时候如果我们需要指定profileTest1为激活状态，那么我们就可以在settings.xml中定义activeProfiles，具体定义如下：

```xml
<activeProfiles> 
    <activeProfile>profileTest1</activeProfile> 
</activeProfiles> 
```
　　考虑这样一种情况，我们在activeProfiles下同时定义了多个需要激活的profile。这里还拿上面的profile定义来举例，我们定义了同时激活profileTest1和profileTest2。

```xml
<activeProfiles> 
    <activeProfile>profileTest1</activeProfile> 
    <activeProfile>profileTest2</activeProfile> 
</activeProfiles>
```
　　从profileTest1和profileTest2我们可以看出它们共同定义了属性hello。那么这个时候我在pom.xml中使用属性hello的时候，它到底取的哪个值呢？是根据activeProfile定义的顺序，后面的覆盖前面的吗？根据我的测试，答案是非也，它是根据profile定义的先后顺序来进行覆盖取值的，然后后面定义的会覆盖前面定义的。
####  使用-P参数显示的激活一个profile

　　我们在进行Maven操作时就可以使用-P参数显示的指定当前激活的是哪一个profile了。比如我们需要在对项目进行打包的时候使用id为profileTest1的profile，我们就可以这样做：

```shell
mvn package –P profileTest1 
```
　　当我们使用activeByDefault或settings.xml中定义了处于激活的profile，但是当我们在进行某些操作的时候又不想它处于激活状态，这个时候我们可以这样做：

```shell
mvn package –P !profileTest1
```
　　这里假设profileTest1是在settings.xml中使用activeProfile标记的处于激活状态的profile，那么当我们使用`-P !profile`的时候就表示在当前操作中该profile将不处于激活状态。
####  根据环境来激活profile

　　profile一个非常重要的特性就是它可以根据不同的环境来激活，比如说根据操作系统的不同激活不同的profile，也可以根据jdk版本的不同激活不同的profile，等等。

```xml
<profiles> 
    <profile> 
        <id>profileTest1</id> 
        <jdk>1.5</jdk> 
    </profile> 
<profiles> 
```
## 查看当前处于激活状态的profile
　　我们可以同时定义多个profile，那么在建立项目的过程中，到底激活的是哪一个profile呢？Maven为我们提供了一个指令可以查看当前处于激活状态的profile都有哪些，这个指令就是`mvn help:active-profiles`。

## 总结
   	profile可以看作是pom的一部分.简单来说,profile支持定义一系列的配置信息,然后在不同的环境中,可以自动触发不同的配置. 比如, 在windows下是一套配置, 在linux下是另一套配置.

?	可以选择在多个地方定义 profile. 在不同地方定义, 作用范围不同. 针对某个项目的配置, 可以写在 pom.xml中. 针对某个用户的配置, 可以在用户目录下的 .m2目录下的 setting.xml 文件中定义. 针对全局的配置, 可以在maven安装目录下的 conf目录中的 setting.xml 文件中定义.

?	profile中能定义的配置信息与所处位置相关. 如果是在settings.xml中, 是全局意义的, 只能定义一些相对而言作用范围较广的配置, 比如`<repositories>, <pluginRepositories>, <properties>`.  定义在`<properties>`中的键值对可以在pom.xml中使用.

?	如果是在pom.xml中, 可以根据项目的不同来定义不同的细节配置信息. 主要有:` <repositories>, <pluginRepositories>, <dependencies>, <plugins>, <properties>, <dependencyManagement>, <distributionManagement>, <build>`下的子元素.

?	profile有多种不同的激活方式. 1) 在profile的`<activation>`下, 将`<activeByDefault>`元素的值设为true, 就表示没有指定其他profile为激活状态时, 默认激活该profile.   2) 在settings.xml中使用<activeProfiles>指定自动激活的profile名. 这样的profile在所有情况下都处于激活状态. 3) 显式命令使用-p选项,指定profile.  4) 根据不同的环境来激活, 如jdk版本, 操作系统, 系统属性, 5) 根据文件是否存在来激活.

?	可以使用 `mvn help: active-Profiles`来查看处于激活状态的profiles.

