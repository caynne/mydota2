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
import requests
import os
import ConfigParser


'''
设置常量
'''
global DAYS
cf = ConfigParser.ConfigParser()
cf.read('config.conf')
DAYS = cf.getint('constant','DAYS')
friden = {"brave":169478997,"bear":337190674,"monkey1":131173904,"man":284155258,"beard":245587068,"ass":123343610,'monkey2':336778995}


'''
初始化api
'''
api = dota2api.Initialise('548C0DBC83E2510AE245A6E1AFCCB5BA')

'''
通过英雄id获得对应英雄名
'''
def getHeroName(id):
    heroId = api.get_heroes()
    # if(id >= 30):
    #     name = heroId['heroes'][id-2]['localized_name']
    # else:
    #     name = heroId['heroes'][id-1]['localized_name']

    for i in xrange(0,114):
        if (heroId['heroes'][i].has_key('id') and heroId['heroes'][i]['id'] == id):
            name = heroId['heroes'][i]['localized_name']
            return name

'''
获取DAYS日内的比赛,以列表返回
'''
def getMatchByLatest7Days(accountId,):
    matchList = []
    match = api.get_match_history(account_id=accountId)
    #获得七天前的时间
    sevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days = DAYS))
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
返回形式  key:英雄名 value:[玩的次数,胜的场数]
'''
def getHeroPool(accountId):
    heroPool = {}#key:英雄名 value:[玩的次数,胜的场数]

    match = getMatchByLatest7Days(accountId)
    for x in xrange(0,len(match)):
        player = match[x]['players']
        matchId = match[x]['match_id']

        for y in xrange(0,len(player)):
            if int(accountId) == player[y]['account_id']:
                heroName = getHeroName(player[y]['hero_id'])
                heroName = cf.get('heroname',heroName)
                if not heroPool.has_key(heroName):
                    heroPool[heroName] = [0,0]
                heroPool[heroName][0] += 1
                if getRainantorDire(matchId,accountId) != getWinorLossByMatchId(matchId):
                    heroPool[heroName][1] += 1

    return heroPool

def getAccountHeroPool():
    accountHeroPool = {}
    for k,v in friden.items():
        heroPool = getHeroPool(v)
        if not accountHeroPool.has_key(k):
            accountHeroPool[k] = heroPool
        accountHeroPool[k] = heroPool
    return accountHeroPool

'''
通过accountId获取用户头像,并写入本地.
格式:用户昵称.jpg
路径:项目文件夹/avatar
todo:用户名为0/0这个的时候,无法保存.提示:No such file or directory: u'/Users/zidongceshi/code/mydota2/avatar/0/0.jpg'
'''
def getAvatarImg(accountId):
    playdetail = api.get_player_summaries(accountId)
    if not len(playdetail['players']):
        return
    imgUrl = playdetail['players'][0]['avatarfull']
    playName = playdetail['players'][0]['personaname']
    imgPath = os.path.join(os.getcwd(),'avatar/')
    if not os.path.exists(imgPath):
        os.mkdir(imgPath)
    if os.path.exists(imgPath+playName+'.jpg'):
        os.remove(imgPath+playName+'.jpg')
    r = requests.get(url=imgUrl)
    f = open(imgPath+playName+'.jpg',mode='wb')
    f.write(r.content)
    f.close()

'''
获取最近七天跟你一起打过（队友或对手）的人的accountId
'''
def getPlayerId():
    accountIdList = []
    for k,v in friden.items():
        match = getMatchByLatest7Days(v)
        for x in xrange(0,len(match)):
            player = match[x]['players']
            for y in xrange(0,len(player)):
                if player[y]['account_id'] in accountIdList:
                    continue
                else:
                    accountIdList.append(player[y]['account_id'])
    return accountIdList


'''
todo:Connection aborted.', error(54, 'Connection reset by peer
'''
def getPlayerNickname():
    nickNameList = []
    accountId = getPlayerId()
    for x in accountId:
        playdetail = api.get_player_summaries(x)
        if not len(playdetail['players']):
            continue
        nickNameList.append(playdetail['players'][0]['personaname'])
    return nickNameList

def getFileName():
    path = '/Users/zidongceshi/code/mydota2/avatar'
    pass


'''
下载最近七天队友或对手的头像到本地
'''
def downPlayerAvatarImg():
    accountId = getPlayerId()
    for i in accountId:
        getAvatarImg(i)

def gethowManyGameDoYouPlay(accountId):
    matchList = getMatchByLatest7Days(accountId)
    return len(matchList)

def getMatchDetailInfo(accountId,matchId):
    matchDetail = []
    detail = api.get_match_details(matchId)
    x = time.localtime(detail['start_time'])
    starttime = time.strftime('%H.%M',x)
    for j in xrange(0,len(detail['players'])):
        if accountId == detail['players'][j]['account_id']:
            try:
                heroName = cf.get('heroname',detail['players'][j]['hero_name'])
            except:
                continue
            kills = detail['players'][j]['kills']
            death = detail['players'][j]['deaths']
            assist = detail['players'][j]['assists']
            lastHit = detail['players'][j]['last_hits']
            xpm = detail['players'][j]['xp_per_min']
            gpm = detail['players'][j]['gold_per_min']
            matchDetail = [float(starttime),kills,death,assist,lastHit,xpm,gpm,heroName,]
            break
    return matchDetail

if __name__ == '__main__':
    getAvatarImg(friden['beard'])
    pass