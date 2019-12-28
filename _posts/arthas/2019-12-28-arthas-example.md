---
layout: post
title: arthas性能调优分析举例
categories: [java]
description: 性能调优分析举例。
keywords: 在线性能调优 , arthas , jvm
---

arthas是阿里开源的线上性能调优利器,有中文文档可供参考学习,https://alibaba.github.io/arthas/install-detail.html

# 性能调优分析举例

## 某页面刷新性能调优

    背景: 某页面数据库条数20万+ , 页面刷新时需要10秒以上

## 首先初步定位

    由于是刷新按钮,会进入bos框架的XxxPageRefresh类,此时可以使用工具arthas进行追踪
    使用trace命令可以查看类中哪些方法可能被调用,甚至方法消耗的时间都会被打印出来,具体如下

在linux命令行arthas目录执行 java -jar arthas-boot.jar ,接着选择对应的进程id,最后进入arthas命令行

输入如下命令(介绍: trace 全类名 星号代表所有方法 , 打印结果如下) 
```shell
$ trace com.xxx.yyy.zzz.XxxPageRefresh *   
Press Q or Ctrl+C to abort.
Affect(class-cnt:1 , method-cnt:3) cost in 211 ms.
```
此时我们只要在点击刷新按钮,就可能会打印如下内容
```shell
`---ts=2019-12-02 11:09:29;thread_name=DubboServerHandler-172.19.0.1:20880-thread-151/traceId:4d56a800d72a8000/time:1575256169282;id=37e;is_daemon=true;priority=5;TCCL=sun.misc.Launcher$AppClassLoader@18b4aac2
    `---[10635.845458ms] com.xxx.yyy.zzz.XxxPageRefresh:doSomething() #这是入口方法,下面都是该方法内的方法,层级很明确
        +---[0.01632ms] com.xxx.yyy.zzz.XxxPageRefresh:getView() #32
        +---[0.014282ms] com.xxx.mmm.ViewPage:getTreeViewPage() #35
        +---[5.047444ms] com.xxx.mmm.ViewPage:clearSelection() #39
        `---[10630.37844ms] com.xxx.mmm.ViewPage:XxxPageRefresh() #40   一般耗时最多的方法会被标红
```  
    此时已经可以完全确认,刷新就是最耗性能的方法
    
**注意**:  如果此时发现没有任何输出,那就表示该类的方法没有被调用,那就重新找到你认为会进入的类的方法进行追踪

## 继续定位追踪(循环过程)
```shell
    介绍: 此时已经可以确定进入类 IViewPage的方法 XxxPageRefresh ,则可以不用星号
$ trace com.xxx.mmm.ViewPage XxxPageRefresh
Press Q or Ctrl+C to abort.
Affect(class-cnt:2 , method-cnt:2) cost in 334 ms.
```
**点击刷新按钮**
```shell
`---ts=2019-12-02 13:55:24;thread_name=DubboServerHandler-172.19.0.1:20880-thread-194/traceId:4d5c9000e636b000/time:1575266124487;id=3d4;is_daemon=true;priority=5;TCCL=sun.misc.Launcher$AppClassLoader@18b4aac2
    `---[3727.943775ms] com.xxx.mvc.list.XViewPage:XxxPageRefresh()
        +---[0.030719ms] com.xxx.mvc.list.XViewPage:isNeedXxxPageRefreshTree() #118
        +---[0.020451ms] com.xxx.mvc.list.XViewPage:XxxPageRefreshTreeView() #119
        +---[0.003388ms] com.xxx.mvc.list.XViewPage:getControl() #122
        +---[1.756648ms] com.xxx.filter.FilterContainer:XxxPageRefresh() #125
        +---[3725.926844ms] com.xxx.mvc.list.AbstractViewPage:XxxPageRefresh() #128
        |   `---[3725.265679ms] com.xxx.mvc.list.AbstractViewPage:XxxPageRefresh()
        |       +---[0.003695ms] com.xxx.list.ControlContext:getBillListId() #376
        |       +---[0.003427ms] com.xxx.mvc.list.AbstractViewPage:getControl() #376
        |       +---[0.211862ms] com.xxx.mvc.list.AbstractViewPage:getSelectedMainOrgIds() #378
        |       +---[0.05223ms] com.xxx.BillPage:setSelectedMainOrgIds() #378
        |       `---[3724.85784ms] com.xxx.BillPage:bindData() #379  这里有进一步找到耗时方法
        `---[0.010922ms] com.xxx.mvc.list.XViewPage:XxxPageRefreshQingView() #129
```
**循环往复的追踪过程**
下面共追踪了8次,每次只截取了最耗时的一行
```shell
+---[9026.036944ms] com.xxx.BillPage:getListData() #2716
+---[6588.815953ms] com.xxx.BillPage:getData() #2246
+---[8219.495835ms] com.xxx.entity.datamodel.IListModel:getData() #2044
 +---[7061.802945ms] com.xxx.entity.list.IListDataProvider:getData() #526
 +---[7436.476284ms] com.xxx.entity.list.IQuery:getData() #261
+---[7088.654679ms] com.xxx.list.query.impl.IdQuery:queryDB() #90
`---[5295.820831ms] com.xxx.orm.ORM:queryDB() #190
`---[7643.377622ms] com.xxx.db.DBExt:queryDB() #413
```
**定位到这个位置的时候,根据经验判断,这时会执行某些SQL语句,那基本可以认为是SQL太慢导致刷新性能问题**
如果这时你有本地环境,那OK了,直接debug调试,看看执行什么SQL,然后解决问题

**如果是线上呢,你也没法debug,怎么办?arthas帮你搞定**

## 使用arthas的watch命令查看方法调用的参数
介绍: watch  全类名  方法  "{params}" 固定写法(具体参考教程) -s表示方法调用后 -x 4表示参数打印的层数 -n表示跟踪的次数 '#cost>100'表示耗时超过100毫秒的才追踪打印
```shell
$ watch com.xxx.db.DBExt queryDB "{params}" -s -x 4 -n 10000 '#cost>100'
Press Q or Ctrl+C to abort.
Affect(class-cnt:1 , method-cnt:1) cost in 190 ms.
ts=2019-12-02 14:36:18; [cost=6134.645861ms] result=@ArrayList[
    @Object[][
        @String[com.xxx.list.query.impl.IdQuery],
        @DBroad[
            other=@DBroad[
                other=@DBroad[({})],
                basedata=@DBroad[basedata({})],
                base=@DBroad[basedata({})],
                main=@DBroad[basedata({})],
                workflow=@DBroad[wf({})],
                log=@DBroad[log({})],
                permission=@DBroad[permission({})],
                qing=@DBroad[qing({})],
                sharedDBroadMap=@ConcurrentHashMap[isEmpty=false;size=12],
                routeKey=@String[],
                tableRouteMap=null,
            ],
           ...很多其他参数
        ],
        @String[/*ORM*/ SELECT field1,field1,field1,field1 FROM table_name_l A\r\nLEFT JOIN table_name_lentry B ON B.FId=A.FId\r\nWHERE A.fbilltypeid = ?\r\nORDER BY A.fbillno DESC],
        ...很多其他参数,
    ],
]
```
打印如上,发现了SQL语句
到这里已经找到根本原因,就是SQL非常耗时,那问题找到了,就得具体问题具体分析

## SQL分析

根据不同的数据库有不同的分析方式(大同小异)

以下是PostgreSQL的分析
```sql
v7pg=> **explain (analyze,verbose,timing,costs,buffers)** SELECT field1,field1,field1,field1 FROM table_name_l A LEFT JOIN table_name_lentry B ON B.FId=A.FId WHERE A.fbilltypeid = 'table_name_ld' ORDER BY A.fbillno DESC limit 10000;
                                                                                 QUERY PLAN

---------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------
 Limit  (cost=38229.82..38254.82 rows=10000 width=74) (actual time=9509.114..9511.522 rows=10000 loops=1)
   Output: fieldn fieldn fieldn fieldn fieldm fieldn fieldm fieldn b.f
allamountfor, fieldm b.fallamount
   Buffers: shared hit=3 read=19260
   ->  Sort  (cost=38229.82..38778.46 rows=219458 width=74) (actual time=9509.109..9510.903 rows=10000 loops=1)
         Output: fieldn fieldn fieldn fieldn fieldm fieldn fieldm b.fdisamoun
t, fieldn fieldm b.fallamount
         Sort Key: a.fbillno DESC
         Sort Method: top-N heapsort  Memory: 3398kB
         Buffers: shared hit=3 read=19260
         ->  Hash Right Join  (cost=2017.14..22552.06 rows=219458 width=74) (actual time=151.222..701.738 rows=214561 loops
=1)
               Output: fieldn fieldn fieldn fieldn fieldm fieldn fieldm b.fdi
samount, fieldn fieldm b.fallamount
               Inner Unique: true
               Hash Cond: (b.fid = a.fid)
               Buffers: shared hit=3 read=19260
               ->  Seq Scan on jdy_dev_151.table_name_lentry b  (cost=0.00..19958.69 rows=219469 width=49) (actual time=0.
075..403.442 rows=214821 loops=1)
                     Output: fieldn fieldn fieldn fieldn fieldn fieldn b.fallamountfo
r, fieldn b.fid
                     Buffers: shared hit=2 read=17762
               ->  Hash  (cost=1758.08..1758.08 rows=20725 width=33) (actual time=151.058..151.060 rows=20725 loops=1)
                     Output: fieldm fieldm a.fbillno
                     Buckets: 32768  Batches: 1  Memory Usage: 1689kB
                     Buffers: shared hit=1 read=1498
                     ->  Seq Scan on jdy_dev_151.table_name_l a  (cost=0.00..1758.08 rows=20725 width=33) (actual time=0.0
80..129.830 rows=20725 loops=1)
                           Output: fieldm fieldm a.fbillno
                           Filter: (a.fbilltypeid = 'table_name_outbound'::citext)
                           Rows Removed by Filter: 1
                           Buffers: shared hit=1 read=1498
 Planning Time: 1.488 ms
 Execution Time: 9512.378 ms
(27 rows)

Time: 9515.867 ms (00:09.516)
v7pg=>
```

## 分析可能是没有建立索引

A.fbilltypeid = 'table_name_outbound' ORDER BY A.fbillno 这两处没有使用到索引
查看相关的表table_name_l发现确实没有建立索引

建立两个索引

CREATE INDEX idx_table_name_l_fbilltypeid ON table_name_l (fbilltypeid);    
CREATE INDEX idx_table_name_l_fbillno ON table_name_l (fbillno);  

再次测试刷新功能,只需要1秒左右就能正常显示

## 小结

本次分析中,主要用到了arthas作为分析工具,使用的命令是 trace , watch 这是两个比较常用的命令, 整体过程基本是反复定位不同的方法,最后找到耗时的具体位置,然后具体问题具体分析,比如可能是循环问题,在大循环中访问数据库,或者是访问远程其他服务,或者时超时等待,本次定位相对比较简单,属于固定情况,在大数据量下数据库没有建立索引导致SQL查询慢,建立索引问题基本解决. 定位的过程基本类似,当然还是需要灵活处理具体问题,这样才能更快解决.