#!/usr/bin/env python
# encoding=utf-8

import dota2api
import time
import datetime
from collections import Counter

api = dota2api.Initialise('548C0DBC83E2510AE245A6E1AFCCB5BA')

match = api.get_match_history(account_id=245587068)

def getPlayTime(star,over):
    for i in xrange(100):
        dataStamp = match['matches'][i]['start_time']
        data = time.localtime(dataStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", data)
        timeList.append(otherStyleTime)

def getPlayHero():
    heroName = []
    for i in xrange(100):
        players = match['matches'][i]['players']
        for j in xrange(10):
            if 245587068 == players[j]['account_id']:
                heroId = players[j]['hero_id']
                heroName.append(getHeroName(int(heroId)))
    return heroName


def analysisPlayHero():
    playHero = getPlayHero()
    list = set(playHero)
    list = sorted(list,key=lambda d:d[1],reverse=True)
    for item in list:
        print 'you playd %s:%d' % (item,playHero.count(item))

def getHeroName(id):
    heroId = api.get_heroes()
    # if(id >= 30):
    #     name = heroId['heroes'][id-2]['localized_name']
    # else:
    #     name = heroId['heroes'][id-1]['localized_name']

    for i in xrange(112):
        if (heroId['heroes'][i].has_key('id') and heroId['heroes'][i]['id'] == id):
            name = heroId['heroes'][i]['localized_name']
    return name

def getMatchByLatest7Days(accountId):
    matchList = []
    match = api.get_match_history(account_id=accountId)
    #获得七天前的时间
    sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 7))
    sevenDayAgoTimeStamp = int(time.mktime(sevenDayAgo.timetuple()))
    for x in xrange(0,len(match['matches'])):
        if sevenDayAgoTimeStamp <= match['matches'][x]['start_time']:
            matchList.append(match['matches'][x])

    return matchList

def WinorLoss(accountId):
    matchList = getMatchByLatest7Days(accountId)
    matchId = []
    record = []
    for x in xrange(0,len(matchList)):
        matchId.append(matchList[x]['match_id'])

    for id in matchId:
        detail = api.get_match_details(match_id=id)
        for i in range(0,9):
            Id = detail['players'][i]
            if Id['account_id'] == accountId and i <= 4:
                flag = 0 # 0:近卫 1:天灾
                break
            else:
                flag = 1
        if detail['radiant_win'] and flag == 0:
            record.append('win')
        elif detail['radiant_win'] and flag == 1:
            record.append('loss')
        elif not detail['radiant_win'] and flag == 0:
            record.append('loss')
        elif not detail['radiant_win'] and flag == 1:
            record.append('win')
    return record


friden = {"brave":169478997,"bear":337190674,"monkey":131173904,"man":284155258,"beard":245587068,"ass":123343610}

if __name__ == '__main__':
    for k,v in friden.items():
        temp = WinorLoss(v)
        count = Counter(temp)
        winTime = count['win']
        lossTime = count['loss']
        txt = "{0}在最近的30天内,你总共赢了:{1}场,输了:{2}场~~".format(k,winTime,lossTime)
        print txt
