#!/usr/bin/env python
#coding: utf-8
__author__ = 'zhanghe'
import urllib2
import re
import json

class NLPJOB:
    def __init__(self,pageIdx=1):
        self.pageIdx = pageIdx
        self.html = ""
        self.job = {}

    def getHtmlFromPageIdx(self):
        try:
            url = "http://www.nlpjob.com/job/"+str(self.pageIdx)+"/"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            self.html = response.read()
        except urllib2.URLError, e:
            return -1

    def getJobInfoFromHtml(self):
        if self.html == "":
            return
        jobCategoryPattern = '<div.*?id="categs-nav.*?>.*?<ul>.*?<li.*?id=.*?class="selected">.*?<a.*?title="(.*?)">.*?'
        partOrFullTimePattern = '<div.*?id="job-details.*?<h2>.*?<img.*?alt="(.*?)".*?'
        jobTitlePattern = '>(.*?)</h2>.*?'
        companyAndLocationPattern = '<p>.*?<span.*?class="fading.*?(?:<strong>(.*?)</strong>|<a.*?>(.*?)</a>).*?<strong>(.*?)</strong>.*?</p>.*?'
        jobDescPattern = '<div.*?id="job-desc.*?>(.*?)</div>.*?'
        jobPubTimePattern = '<div.*?id="number-views.*?<strong>(.*?)</strong>'

        pattern = re.compile(jobCategoryPattern+partOrFullTimePattern+jobTitlePattern+companyAndLocationPattern+jobDescPattern+jobPubTimePattern,re.S)
        jobs = re.findall(pattern,self.html)

        self.job["category"] = jobs[0][0].strip()
        self.job["time-type"] = jobs[0][1].strip()
        self.job["title"] = jobs[0][2].strip()
        self.job["company"] = jobs[0][3].strip()+jobs[0][4].strip()
        self.job["location"] = jobs[0][5].strip()
        self.job["description"] = jobs[0][6]\
            .replace("<br />","")\
            .replace("</span>","")\
            .replace("<span class=\"caps\">","")\
            .replace("\n","")\
            .replace("\t","")\
            .strip()
        self.job["publish-time"] = jobs[0][7].strip()

    def saveJobInfoAsJson(self):
        encodejson = json.dumps(self.job,ensure_ascii=False,indent=4)
        filename = "nlpjob_data/"+str(self.pageIdx)+".txt"
        f = open(filename,'w')
        f.write(encodejson)
        f.close()

log = open("nlpjob_data/log.txt",'w')
for pageIdx in xrange(7426,17203):
    crawler = NLPJOB(pageIdx)
    print "proccessing page "+str(pageIdx)+"...",
    if(crawler.getHtmlFromPageIdx() != -1):
        crawler.getJobInfoFromHtml()
        crawler.saveJobInfoAsJson()
        print "success"
        log.write("Proccessing page:"+str(pageIdx)+"\tSuccess\n")
    else:
        print "fail"
        log.write("Proccessing page:"+str(pageIdx)+"\tFail\n")
log.close()