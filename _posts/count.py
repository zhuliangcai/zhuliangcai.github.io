#!/usr/bin/env python3
# coding:utf-8
"""统计文件数量
"""

# end_pymotw_header
import os

count = 0

def list_files(path):
    global count
    #print(path)
    files = os.listdir(path)
    for name in files:
        file = path+'\\'+name
        # print(file)
        if os.path.isdir(file):
            list_files(file)
        else:
            print(name)
            count=count + 1
    return count


pwd = os.getcwd()
# print(pwd) # F:\git\zhuliangcai.github.io\_posts

file_counts = list_files(pwd)

print(file_counts)








