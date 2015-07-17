#!/usr/bin/env python
#coding: utf-8
__author__ = 'zhanghe'
#7426-17189
#http://www.nlpjob.com/job/7426/
import urllib2
url = "http://www.nlpjob.com/job/7426/"
request = urllib2.Request(url)
response = urllib2.urlopen(request)
html = response.read()
print html