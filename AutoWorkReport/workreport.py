import requests
import json
import time
from datetime import timedelta, date
import operator
from lxml import etree
from selenium import webdriver

class WorkReport:
    # 默认请求头
    _headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    def DateToStamp(self, date):
        strDate = date.strftime("%Y-%m-%d %H:%M:%S")
        timeArray = time.strptime(strDate, "%Y-%m-%d %H:%M:%S")
        return int(round(time.mktime(timeArray) * 1000))

    def StrToStamp(self, strDate):
        timeArray = time.strptime(strDate, "%Y-%m-%d %H:%M:%S")
        return int(round(time.mktime(timeArray) * 1000))


    def work(self):
        strUrl = "https://jzcz.teamcola.com/login/"
        postData = 'timezone=8&data=%7B%22username%22%3A%22zhaok%40china-creative.net%22%2C%22password%22%3A%22hotmail%22%7D'

        session = requests.session()

        req = session.post(strUrl, postData, headers=self._headers)
        strHtml_code = req.text

        # print(strHtml_code)

        strHtml_code.index('success')

        dateMax = date.today()+timedelta(days=1)
        date0 = date.today()
        date1 = date.today()-timedelta(days=1)
        date2 = date.today()-timedelta(days=2)
        date3 = date.today()-timedelta(days=3)
        date4 = date.today()-timedelta(days=4)
        date5 = date.today()-timedelta(days=5)
        date6 = date.today()-timedelta(days=6)
        date7 = date.today()-timedelta(days=7)
        date8 = date.today()-timedelta(days=8)
        date9 = date.today()-timedelta(days=9)
        date10 = date.today()-timedelta(days=10)

        startDate = self.DateToStamp(date10)  #时间检索访问
        endDate = self.DateToStamp(dateMax)

        dayKeys = []
        dayKeys.append(self.DateToStamp(date0)) 
        dayKeys.append(self.DateToStamp(date1)) 
        dayKeys.append(self.DateToStamp(date2)) 
        dayKeys.append(self.DateToStamp(date3)) 
        dayKeys.append(self.DateToStamp(date4)) 
        dayKeys.append(self.DateToStamp(date5)) 
        dayKeys.append(self.DateToStamp(date6)) 
        dayKeys.append(self.DateToStamp(date7)) 
        dayKeys.append(self.DateToStamp(date8)) 
        dayKeys.append(self.DateToStamp(date9)) 
        dayKeys.append(self.DateToStamp(date10)) 

        strUrl = "https://jzcz.teamcola.com/worklog/"
        postData = "timezone=8&data=%7B%22start%22%3A{startDate}%2C%22end%22%3A{endDate}%7D"
        postData = postData.format(startDate=startDate, endDate=endDate)
        # print(postData)
        req = session.post(strUrl, postData, headers=self._headers)
        strHtml_code = req.text

        strHtml_code.index('success')

        # print(strHtml_code)

        jsonData = json.loads(strHtml_code)
        worklogs = jsonData['worklogs']
        lastWorklog = {}

        #今天已经填写
        if len(worklogs[str(dayKeys[0])]) != 0:
            print(date.today().strftime("%Y-%m-%d ") + '已经填完日志')
            return

        #找到最近一天填写
        for i in range(1,11):
            if len(worklogs[str(dayKeys[i])]) != 0:
                lastWorklog = worklogs[str(dayKeys[i])]
                break
        #10天找不到，手动填一条        
        if not lastWorklog:
            print("10天都找不到，手动写一条日志吧")
            return

        workData = lastWorklog[0]

        tree = etree.HTML(workData["html_content"])

        content = tree.xpath('//p/text()')[0]   #<p>开发</p>\n
        team_id = workData["team_id"]
        label_id = workData["labels"][0]["guid"]

        strUrl = "https://jzcz.teamcola.com/worklog/add"
        #上午
        startTime = self.StrToStamp(date0.strftime("%Y-%m-%d 09:00:00"))
        endTime = self.StrToStamp(date0.strftime("%Y-%m-%d 12:00:00"))

        postWork = "timezone=8&data=%7B%22content%22%3A%22{content}%22%2C%22team%22%3A%22{team}%22%2C%22labels%22%3A%5B%22{labels}%22%5D%2C%22start%22%3A{start}%2C%22end%22%3A{end}%7D"
        postWork = postWork.format(content=content, team=team_id,labels=label_id,start=startTime,end=endTime)
        postWork = postWork.encode("utf-8")

        req = session.post(strUrl, postWork, headers=self._headers)
        strHtml_code = req.text

        strHtml_code.index('success')

        #下午
        startTime = self.StrToStamp(date0.strftime("%Y-%m-%d 13:00:00"))
        endTime = self.StrToStamp(date0.strftime("%Y-%m-%d 18:00:00"))

        postWork = "timezone=8&data=%7B%22content%22%3A%22{content}%22%2C%22team%22%3A%22{team}%22%2C%22labels%22%3A%5B%22{labels}%22%5D%2C%22start%22%3A{start}%2C%22end%22%3A{end}%7D"
        postWork = postWork.format(content=content, team=team_id,labels=label_id,start=startTime,end=endTime)
        postWork = postWork.encode("utf-8")

        req = session.post(strUrl, postWork, headers=self._headers)
        strHtml_code = req.text

        strHtml_code.index('success')

        print(date.today().strftime("%Y-%m-%d ") + '填完日志')
        return 200


if __name__ == "__main__":

    report = WorkReport()
    report.work()