# -*-coding:utf-8 -*-
__author__ = 'zhanghe'
import urllib
import urllib2
import re
page = 1
url = 'http://www.qiushibaike.com/hot/page/'+str(page)
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
headers = {'User-Agent':user_agent}
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    content = response.read()
    authorPattern = '<div.*?class="author.*?>.*?<a.*?<img.*?>(.*?)</a>.*?</div>.*?'
    contentAndTimePattern = '<div.*?class="content.*?>(.*?)<!--(.*?)-->.*?</div>.*?'
    statsVotePattern = '<div.*?class="stats-vote.*?>.*?<i.*?class="number.*?>(.*?)</i>.*?'
    pattern = re.compile(authorPattern+contentAndTimePattern+statsVotePattern,re.S)
    items = re.findall(pattern,content)
    for item in items:
        print 'Author:'+item[0].strip()
        print 'Content:'+item[1].strip()
        print 'Time:'+item[2].strip()
        print 'Votes:'+item[3].strip()
except urllib2.URLError, e:
    if hasattr(e,'code'):
        print e.code
    if hasattr(e,'reason'):
        print e.reason

