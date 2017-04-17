#!/usr/bin/env python
# encoding=utf-8

import xlwt
import json
import codecs
import sys
import os
import time
import PIL
from wordcloud import WordCloud
import numpy as np
import sys
import data as d2d
import matplotlib.pyplot as plt
import conn

reload(sys)
sys.setdefaultencoding('utf-8')

friden = {"brave":169478997,"bear":337190674,"monkey":131173904,"man":284155258,"beard":245587068,'monkey2':336778995}

conn = conn.connDB()
cursor = conn.cursor()

def writeHeroPool2csv():
    wb = xlwt.Workbook()
    for k,v in friden.items():
        heroPool = d2d.getHeroPool(v)
        heroPoolJson = json.dumps(heroPool,ensure_ascii=False)
        ws = wb.add_sheet(k,cell_overwrite_ok=True)

        row = 0
        col = 0
        for kk,vv in sorted(heroPool.items(),key=lambda d:d[1],reverse=True):
            ws.write(row,col,kk)
            for i in vv:
                col += 1
                ws.write(row,col,i)
            col = 0
            row += 1
        print k
    wb.save('heroPool.csv')

def writePlayPartyRate2Csv():
    wb = xlwt.Workbook()
    for k,v in friden.items():
        rate = d2d.getPlayPartyWinorLoss(v)
        ws = wb.add_sheet(k,cell_overwrite_ok=True)

        row = 0
        col = 0
        for kk,vv in sorted(rate.items(),key=lambda d:d[0],reverse=False):
            ws.write(row,col,kk)
            for i in vv:
                col += 1
                ws.write(row,col,i)
            col = 0
            row += 1
    wb.save('PlayPartyRate.csv')

def writeWinOrLoss2Csv():
    wb = xlwt.Workbook()
    for k,v in friden.items():
        WinOrLoss = d2d.WinorLoss(v)
        ws = wb.add_sheet(k,cell_overwrite_ok=True)

        row = 0
        col = 0
        for x in WinOrLoss:
            ws.write(row,col,x)
            col = 0
            row += 1
    wb.save('WinOrLoss.csv')

def writePlayPartyRate2Json():
    dict = {}
    for k,v in friden.items():
        rate = d2d.getPlayPartyWinorLoss(v)
        dict[k] = rate
    with open('/Users/zidongceshi/code/mydota2/data/rate.json','wb') as f:
        f.write(json.dumps(dict))

def writeHeroPool2Json():
    dict = {}
    for k,v in friden.items():
        rate = d2d.getHeroPool(v)
        dict[k] = rate
    with open('/Users/zidongceshi/code/mydota2/data/heroPool.json','wb') as f:
        f.write(json.dumps(dict))

def writeWinOrLoss2Json():
    dict = {}
    for k,v in friden.items():
        rate = d2d.WinorLoss(v)
        dict[k] = rate
    with open('/Users/zidongceshi/code/mydota2/data/winOrloss.json','wb') as f:
        f.write(json.dumps(dict))

def writeUserInfo2Json():
    userInfo = {} #最终返回字典,存放想要的数据
    #sql语句用来查询,时间维度:月,指标:场次,胜,胜率
    sql = "select ap.accountid as 'uid',a.nickname,from_unixtime(md.`startTime`,'%Y-%m') as '月份',count(ap.accountid) as'场次',sum(ap.winorloss) as'赢' ,sum(ap.winorloss)/count(ap.accountid) as '胜率'from accountplayed as ap join `matchDetail` as md join account as a on ap.matchid = md.matchid and ap.accountid = a.accountid group by from_unixtime(md.`startTime`,'%Y-%m'),ap.accountid,a.nickname order by from_unixtime(md.`startTime`,'%Y-%m')"
    cursor.execute(sql)
    r1 = cursor.fetchall()
    for k,v in friden.items():
        userInfo[k] = {}
        #ltime:统计时间维度,目前是月
        ltime = []
        #月内,打的场次
        count = []
        #胜率
        rate = []
        #胜场
        win = []
        for item in r1:
            if v == item['uid']:
                ltime.append(item['月份'])
                win.append(int(item['赢']))
                rate.append(float(item['胜率']))
                count.append(item['场次'])
        userInfo[k]['wDautime'] = ltime
        userInfo[k]['wDauwin'] = win
        userInfo[k]['wDauCount'] =  count
        userInfo[k]['wDauRatet'] =  rate
        print k
        userInfo[k]['username'] = k
        userInfo[k]['howmany'] = d2d.gethowManyGameDoYouPlay(v)
        userInfo[k]['win'] = d2d.WinorLoss(v).count('win')
        userInfo[k]['loss'] = d2d.WinorLoss(v).count('loss')
        userInfo[k]['heropool'] = d2d.getHeroPool(v)
        userInfo[k]['playparty'] = d2d.getPlayPartyWinorLoss(v)
    dirPath = os.path.join(os.getcwd(),'data')
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    filePath = os.path.join(dirPath,time.strftime('%Y%m%d',time.localtime(time.time())))
    filePath = filePath +'.json'
    with open(filePath,'wb') as f:
        f.write(json.dumps(userInfo))

#生成最近对队对手昵称的词云图
def worldcloud():
    nickname = d2d.getPlayerNickname()
    strNickName = ' '.join(nickname)
    dirPath = os.path.join(os.getcwd(),'data')
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    filePath = os.path.join(dirPath,'nickname.png')
    wordcloud = WordCloud(font_path='/Users/zidongceshi/code/mydota2/MSYH.TTF',
                          background_color='white',
                          width=800,
                          height=600,
                          #margin=1,
                          #mask=alice_mask,
                          max_words=2000,
                          max_font_size=60,
                          random_state=42)
    wordcloud = wordcloud.generate(strNickName)
    plt.imshow(wordcloud)
    plt.axis('off')
    #plt.show()
    plt.savefig(filePath)

def writeMatchDetail2Json():
    matchDetail = {}
    for k,v in friden.items():
        matchId = []
        matchDetails = []
        print k
        matchList = d2d.getMatchByLatest7Days(v)
        for x in xrange(0,len(matchList)):
            matchId.append(matchList[x]['match_id'])
        for id in matchId:
             matchDetails.append(d2d.getMatchDetailInfo(v,id))
        matchDetail[k] = matchDetails
    dirPath = os.path.join(os.getcwd(),'data')
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    filePath = os.path.join(dirPath,time.strftime('%Y%m%d',time.localtime(time.time()))+'matchdetail')
    filePath = filePath +'.json'
    with open(filePath,'wb') as f:
        f.write(json.dumps(matchDetail))

def writePlayPartyDetail2Json():
    playPartyDetail = {}
    for k,v in friden.items():
        print k
        playPartyDetail[k] = d2d.getPlayPartyWinorLoss(v)
    dirPath = os.path.join(os.getcwd(),'data')
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    filePath = os.path.join(dirPath,time.strftime('%Y%m%d',time.localtime(time.time()))+'PlayPartyDetail')
    filePath = filePath +'.json'
    with open(filePath,'wb') as f:
        f.write(json.dumps(playPartyDetail))

def run():
    #writePlayPartyRate2Csv()
    #writeHeroPol2csv()
    writeUserInfo2Json()
    #worldcloud()
    #writeMatchDetail2Json()
    writePlayPartyDetail2Json()

if __name__ == "__main__":
    run()
