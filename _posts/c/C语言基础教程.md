---
layout: post
title: C语言基础教程
categories: [C, c,c语言]
description: C语言基础教程
keywords: C, c,c语言
---

C语言基础教程

## 编程工具CLion

下载并安装 Dev-Cpp 会得到gcc编译环境 MinGW64
jetBrains官网下载，正常安装即可

## Hello world

新建C99项目，会自动生成 main.c 文件，内容如下
```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```
build项目后，Run对应的项目即可

## 数值、字符与字符串

- | 类型 | 描述 
:-: | :-: | :-:
数值 | int | 存储整数
- | float| 整数+小数
- | double| 整数+小数(精度更高)
字符 | char | 单个字符
- | 字符串| 一段连续的字符

## 声明方式

数据类型 变量名;

举例： 
```cpp 
// int类型 int i; 
/* 普通声明 */ 
int j,k; 
/* 同时声明多个 */ 
int age= 18; 
/* 声明的同时赋值 */ 
int Alan ,Sam=16;/* 声明与同时赋值 */ 
// float类型 float f; /* 普通声明 */ 
float q,money; /* 同时声明多个 */ 
float v = 2.0; /* 声明的同时赋值 */ 
// char类型 
char c; /*普通声明 */ 
char zh,text; /* 同时声明多个 */ 
char letter = 'A'; 
/* 声明的同时赋值 */ // char数组(字符串) 
char c[20] = { 'H','e','l','l','o',' ','w','o','r','l','d' }; 
char name[] = { 'A', 'l', 'a', 'n' }; 
```

## 转义字符

在一段字符串中，不能直接出现，需要转义的字符，例如：

'\n' 换行 '\t'' 水平制表 '\'' 单引号 '\"' 双引号 '\' 反斜杠
```c
#include<stdio.h>
main()
{
    printf("Num\tName\n");
    printf("001\tAlan\n");
    printf("002\tLellansin\n");
}
```

输出结果：
```shell
Num　　　Name
001　　　Alan
002　　　Lellansin
```