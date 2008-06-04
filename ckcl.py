#!/usr/bin/env python
#coding=utf-8
import re
file = open('/home/malijun/桌面/xml.txt','r')
out_file = open('out.txt','w')
for line in file.readlines():
    out_file.write(re.sub('[a-z]','',line[:-1]+'\n'))
file.close()
out_file.close()