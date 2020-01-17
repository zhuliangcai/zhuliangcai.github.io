```mermaid
graph LR
A[Arthas] --> B(基础命令)
A --> C(class相关)
A --> D(jvm相关)
A --> E(字节码增强)

B --> B1[help 查看命令帮助信息]
B --> B2[cls 清空当前屏幕区域]
B --> B3[session 查看当前会话的信息]
B --> B4[reset 重置增强类，将被Arthas增强过的类全部还原，Arthas服务端关闭时会重置所有增强过的类]
B --> B5[version 输出当前目标java进程所加载的Arthas版本号]
B --> B6[history 打印命令历史]
B --> B7[quit|exit 退出当前Arthas客户端，其他arthas客户端不受影响]
B --> B8[stop 和shutdown命令一致]
B --> B9[shutdown 关闭arthas服务端，所有arthas客户端全部退出]
B --> B10[keymap Arthas快捷键列表及自定义快捷键 ]
B --> B11[option查看或设置arthas全局开关 ]

C --> C1(sc)
C --> C2(sm)
C --> C3(jad)
C --> C4(mc)
C --> C5(redefine)
C --> C6(dump)
C --> C7(classloder)

D --> D1(dashboard)
D --> D2(thread)
D --> D3(jvm)
D --> D4(sysprop)
D --> D5(sysenv)
D --> D6(vmoption)
D --> D7(logger)
D --> D8(getstatic)
D --> D9(ognl)
D --> D10(mbean)
D --> D11(heapdump)

E --> E1(tt)
E --> E2(watch)
E --> E3(monitor)
E --> E4(stack)
E --> E5(trace)
```