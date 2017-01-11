#!/usr/bin/env python
# encoding=utf-8


'''
1 获取英雄池.最近玩的英雄,次数,胜场 getHeroPool(accountId)
2 获取开黑数据总结,getPlayPartyWinorLoss()  开黑规模,胜利场数
3 谁是大腿  whoisbiglag() 返回形式:accountId:[次数,胜场]
4 最近的胜负场数
'''

import dota2api
import time
import datetime
from collections import Counter

api = dota2api.Initialise('548C0DBC83E2510AE245A6E1AFCCB5BA')

match = api.get_match_history(account_id=245587068)
friden = {"brave":169478997,"bear":337190674,"monkey":131173904,"man":284155258,"beard":245587068,"ass":123343610}


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

'''
获取7日内的比赛,以列表返回
'''
def getMatchByLatest7Days(accountId):
    matchList = []
    match = api.get_match_history(account_id=accountId)
    #获得七天前的时间
    sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 17))
    sevenDayAgoTimeStamp = int(time.mktime(sevenDayAgo.timetuple()))
    for x in xrange(0,len(match['matches'])):
        if sevenDayAgoTimeStamp <= match['matches'][x]['start_time']:
            matchList.append(match['matches'][x])

    return matchList

'''
最近accountId的胜负场数
'''
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

#返回此局比赛是天灾胜利还是近卫胜利
def getWinorLossByMatchId(matchId):
    detail = api.get_match_details(match_id=matchId)
    return detail['radiant_win']

#返回此局的accountID是在天灾还是近卫
def getRainantorDire(matchId,accountId):
    detail = api.get_match_details(matchId)
    for i in range(0,9):
        Id = detail['players'][i]
        if Id['account_id'] == accountId and i <= 4:
            flag = 0 # 0:近卫 1:天灾
            break
        else:
            flag = 1
    return flag
'''
获取此局比赛是几人黑
'''
def getplayPartyCount(matchId):
    playAccountList = []#本局10名玩家的id
    playPartner = []#开黑成员
    matchdetail = api.get_match_details(matchId)
    count = 0#统计开黑人数

    player = matchdetail['players']
    for i in xrange(len(player)):
        playAccountList.append(player[i]['account_id'])
    for j in xrange(0,len(playAccountList)):
        if playAccountList[j] in friden.values():
            playPartner.append(playAccountList[j])
            count += 1
    return playPartner


'''
获得开黑数据的总结:单排-->5人黑的次数以及胜利的次数
最终返回此字典,里面有开黑次数:playparty.与开黑胜率的列表:rate
playparty:放入rateCount字典中,index 1到5代表的意思为:单排,2人黑,3人黑,4人黑,5人黑的总共的次数
rate:放入rateCount字典中,index 1到5代表的意思为:单排,2人黑,3人黑,4人黑,5人黑胜利的次数
'''
def getPlayPartyWinorLoss(accountId):
    matchList = getMatchByLatest7Days(accountId)
    rateCount = {'playparty':[],'rate':[]}#最终返回此字典,里面有开黑次数与开黑胜率的列表
    playparty = [0,0,0,0,0]#放入rateCount字典中,index 1到5代表的意思为:单排,2人黑,3人黑,4人黑,5人黑的总共的次数
    rate =[0,0,0,0,0]#放入rateCount字典中,index 1到5代表的意思为:单排,2人黑,3人黑,4人黑,5人黑胜利的次数

    for i in xrange(0,len(matchList)):
        matchId = matchList[i]['match_id']
        playPartner = getplayPartyCount(matchId)
        playerNick = []#开黑成员昵称
        for k,v in friden.items():
            for item in playPartner:
                if item == v:
                    playerNick.append(k)
        partnerCount = len(playPartner)#开黑人数

        #使用异或(xor)来判断此局胜负.  bool(xxx) != bool(xxx)
        WinorLoss =  getRainantorDire(matchId,accountId) !=  getWinorLossByMatchId(matchId)
        if WinorLoss:
            flag = 1
        else:
            flag = 0

        if partnerCount == 1:
            playparty[0] += 1
            if flag:
                rate[0] += 1
            #print '单排,{0}'.format(flag)
        elif partnerCount == 2:
            playparty[1] += 1
            if flag:
                rate[1] += 1
            #print "{0}和{1}两个黑,{2}".format(playerNick[0],playerNick[1],flag)
        elif partnerCount == 3:
            playparty[2] += 1
            if flag:
                rate[2] += 1
            #print "{0},{1}和{2}三个黑,{3}".format(playerNick[0],playerNick[1],playerNick[2],flag)
        elif partnerCount == 4:
            playparty[3] += 1
            if flag:
                rate[3] += 1
            #print "{0},{1},{2},{3}四个黑,{4}".format(playerNick[0],playerNick[1],playerNick[2],playerNick[3],flag)
        elif partnerCount == 5:
            playparty[4] += 1
            if flag:
                rate[4] += 1
            #print "{0},{1},{2},{3},{4}五个黑{5}".format(playerNick[0],playerNick[1],playerNick[2],playerNick[3],playerNick[4],flag)
    rateCount['playparty'] = playparty
    rateCount['rate'] = rate
    return rateCount


'''
跟哪位大神开黑时的胜利次多.
accountId:[次数,胜场]
'''
def whoisbiglag(accountId):
    match = getMatchByLatest7Days(accountId)
    teamMate2 = {'ass':[0,0],'bear':[0,0],'monkey':[0,0],'man':[0,0],'brave':[0,0],'beard':[0,0]}
    teamMate3 = {'ass':[0,0],'bear':[0,0],'monkey':[0,0],'man':[0,0],'brave':[0,0],'beard':[0,0]}
    teamMate4 = {'ass':[0,0],'bear':[0,0],'monkey':[0,0],'man':[0,0],'brave':[0,0],'beard':[0,0]}
    teamMate5 = {'ass':[0,0],'bear':[0,0],'monkey':[0,0],'man':[0,0],'brave':[0,0],'beard':[0,0]}

    for x in xrange(0,len(match)):
        teamMateId = []#队友id
        players = match[x]['players']
        for y in xrange(0,len(players)):
            teamMateId.append(players[y]['account_id'])
        partnerCount = len(getplayPartyCount(match[x]['match_id']))#几人黑


        if partnerCount == 2:
            for k,v in friden.items():
                if v == accountId:
                    continue
                if v in teamMateId:
                    teamMate2[k][0] += 1
                    if getRainantorDire(matchId=match[x]['match_id'],accountId=accountId) != getWinorLossByMatchId(matchId= match[x]['match_id']):
                        teamMate2[k][1] += 1

        elif partnerCount == 3:
           for k,v in friden.items():
                if v == accountId:
                    continue
                if v in teamMateId:
                    teamMate3[k][0] += 1
                    if getRainantorDire(matchId=match[x]['match_id'],accountId=accountId) != getWinorLossByMatchId(matchId= match[x]['match_id']):
                        teamMate3[k][1] += 1

        elif partnerCount == 4:
            for k,v in friden.items():
                if v == accountId:
                    continue
                if v in teamMateId:
                    teamMate4[k][0] += 1
                    if getRainantorDire(matchId=match[x]['match_id'],accountId=accountId) != getWinorLossByMatchId(matchId= match[x]['match_id']):
                        teamMate4[k][1] += 1

        elif partnerCount == 5:
            for k,v in friden.items():
                if v == accountId:
                    continue
                if v in teamMateId:
                    teamMate5[k][0] += 1
                    if getRainantorDire(matchId=match[x]['match_id'],accountId=accountId) != getWinorLossByMatchId(matchId= match[x]['match_id']):
                        teamMate5[k][1] += 1

    result = {'2':teamMate2,'3':teamMate3,'4':teamMate4,'5':teamMate5}
    return result

'''
获取最近玩的英雄,次数,胜场
'''
def getHeroPool(accountId):
    heroPool = {}#key:英雄名 value:countAndWin
    countAndWin = [0,0]

    match = getMatchByLatest7Days(accountId)
    for x in xrange(0,len(match)):
        player = match[x]['players']
        matchId = match[x]['match_id']

        for y in xrange(0,len(player)):
            if accountId == player[y]['account_id']:
                heroName = getHeroName(player[y]['hero_id'])
                if not heroPool.has_key(heroName):
                    heroPool[heroName] = [0,0]
                heroPool[heroName][0] += 1
                if getRainantorDire(matchId,accountId) != getWinorLossByMatchId(matchId):
                    heroPool[heroName][1] += 1

    return heroPool

if __name__ == '__main__':

    #获取7天内胜负场
    # for k,v in friden.items():
    #     temp = WinorLoss(v)
    #     count = Counter(temp)
    #     winTime = count['win']
    #     lossTime = count['loss']
    #     txt = "{0}在最近的7天内,你总共赢了:{1}场,输了:{2}场~~".format(k,winTime,lossTime)
    #     print txt


    #获取开黑胜负场
    # getPlayPartyWinorLoss(123343610)
    # for k,v in friden.items():
    #     rateCount = getPlayPartyWinorLoss(v)
    #     print '{0}:最近单排{1}次,胜{2}场.二人黑{3}次,胜{4}场.三个黑{5}次,胜{6}场.四人黑{7},胜{8}场,五人黑{9}次,胜{10}场'.format(k,rateCount['playparty'][0],rateCount['rate'][0],rateCount['playparty'][1],rateCount['rate'][1],rateCount['playparty'][2],rateCount['rate'][2],rateCount['playparty'][3],rateCount['rate'][3],rateCount['playparty'][4],rateCount['rate'][4])
    #
    # for k,v in friden.items():
    #     result = whoisbiglag(v)
    #     print result
    # for k,v in friden.items():
    #     heroPool = getHeroPool(v)
    #     heroPool = sorted(heroPool.iteritems(),key=lambda d:d[1],reverse=True)
    #     print '{0}最近玩了{1}个英雄'.format(k,len(heroPool))
    #     for x in xrange(len(heroPool)):
    #         print heroPool[x]
    #     print '*'*30
    whoisbiglag(friden['ass'])
