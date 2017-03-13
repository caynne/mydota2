#!/usr/bin/env python
# encoding=utf-8

import conn
import ConfigParser
import dota2api
import sys
import data as d2d
import datetime
import MySQLdb.cursors

reload(sys)
sys.setdefaultencoding('utf-8')

api = dota2api.Initialise('548C0DBC83E2510AE245A6E1AFCCB5BA')

conn = conn.connDB()
cursor = conn.cursor()
cf = ConfigParser.ConfigParser()
cf.read('../config.conf')

friden = {"brave":169478997,"bear":337190674,"monkey":131173904,"man":284155258,"beard":245587068,'''"ass":123343610,''''monkey2':336778995}

def hero2DB():
    heroes = api.get_heroes()
    for i in xrange(0,113):
        heroId = heroes['heroes'][i]['id']
        localized_name = heroes['heroes'][i]['localized_name']
        nickName = cf.get('heroname',localized_name)
        value = [heroId,nickName]
        cursor.execute('INSERT INTO hero (heroId,nickName) values(%s,%s)',value)
        print heroId,nickName
    conn.commit()


'''
数据库中,将时间戳格式化输出,使用from_unxitime(timestamp,'%Y-%m-%d')
'''
def account2DB():
    for name in ['brave','bear','monkey1','man','monkey2','beard']:
        accountId = cf.getint('constant',name)
        playdetail = api.get_player_summaries(accountId)
        if not len(playdetail['players']):
            continue
        avatar = playdetail['players'][0]['avatarfull']
        nickName = playdetail['players'][0]['personaname']
        timeCreated = playdetail['players'][0]['timecreated']
        value = [accountId,str(nickName),str(avatar),timeCreated]
        cursor.execute('INSERT INTO account (accountId,nickName,avatar,timeCreated) values(%s,%s,%s,%s)',value)
        print accountId,nickName,avatar
    conn.commit()

'''
accountId:账号
matchId:比赛编号
heroId:此局比赛使用英雄编号
floor:此局比赛所在楼层
winOrLoss:此局比赛输赢
'''
def played2DB():
    for k,v in friden.items():
        print k
        matchHistory = api.get_match_history(account_id=v)
        for i in xrange(0,100):
            for l in xrange(0,len(matchHistory['matches'])):
                matchId = matchHistory['matches'][l]['match_id']
                for j in xrange(0,10):
                    if v == matchHistory['matches'][l]['players'][j]['account_id']:
                        floor = j+1
                        heroId = matchHistory['matches'][l]['players'][j]['hero_id']
                        break
                if floor >5:
                    isDirOrRadin = 1 #天灾
                else:
                    isDirOrRadin = 0 #近卫
                matchDetail = api.get_match_details(matchId)
                isRadinWin = matchDetail['radiant_win']
                #使用异或(xor)来判断此局胜负.  bool(xxx) != bool(xxx)
                WinorLoss =  isDirOrRadin !=  isRadinWin
                if WinorLoss:
                    flag = 1
                else:
                    flag = 0
                assists = matchDetail['players'][floor-1]['assists']
                deaths = matchDetail['players'][floor-1]['deaths']
                denies = matchDetail['players'][floor-1]['denies']
                heroDamage = matchDetail['players'][floor-1]['hero_damage']
                kills = matchDetail['players'][floor-1]['kills']
                lastHits = matchDetail['players'][floor-1]['last_hits']
                goldSpent = matchDetail['players'][floor-1]['gold_spent']
                goldPerMin = matchDetail['players'][floor-1]['gold_per_min']
                xpPerMin = matchDetail['players'][floor-1]['xp_per_min']
                heroHealing = matchDetail['players'][floor-1]['hero_healing']
                towerDamage = matchDetail['players'][floor-1]['tower_damage']

                value = [v,matchId,heroId,floor,flag,assists,denies,deaths,goldPerMin,kills,lastHits,heroDamage,heroHealing,goldSpent,xpPerMin,towerDamage]
                cursor.execute('INSERT INTO accountPlayed (accountId,matchId,heroId,floor,winOrLoss,assists,denies,deaths,goldPerMin,kills,lastHits,heroDamage,heroHealing,goldSpent,xpPerMin,towerDamage) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
                conn.commit()
            lastHistory = matchHistory['matches'][len(matchHistory['matches'])-1]['match_id']
            matchHistory = api.get_match_history(account_id=v,start_at_match_id=lastHistory)
            if lastHistory == matchHistory['matches'][len(matchHistory['matches'])-1]['match_id']:
                break

def mathcDetail2DB():
    cursor.execute('select  matchId from matchDetail order by  matchid desc limit 1')
    r1 = cursor.fetchall()
    cursor.execute('select  distinct matchId from accountPlayed where matchId > %s' %r1[0]['matchId'] )
    r2 = cursor.fetchall()
    count = 1

    for item in r2:
        detail = api.get_match_details(item['matchId'])
        matchId = detail['match_id']
        startTime = detail['start_time']
        duration = detail['duration'] / 60 #单位:分钟
        firstBloodTime = detail['first_blood_time']
        gameMode = detail['game_mode']

        value = [matchId,startTime,duration,firstBloodTime,gameMode]
        cursor.execute('INSERT INTO matchDetail (matchId,startTime,duration,firstBloodTime,gameMode) values(%s,%s,%s,%s,%s)',value)
        conn.commit()
        count = count + 1
        print count

def writeNewMatch2DB():
    for k,v in friden.items():
        newMatchId = []
        print k
        cursor.execute('SELECT matchId FROM accountPlayed where accountId = %d order by matchID desc limit 1' %v)
        r = cursor.fetchall()
        lastWrite2MathcId = r[0]['matchId']
        matchHistory = api.get_match_history(account_id=v)
        for i in xrange(0,100):
            for kk in xrange(0,100):
                for l in matchHistory['matches']:
                    matchId = l['match_id']
                    if lastWrite2MathcId < matchId and matchId not in newMatchId:
                        newMatchId.append(matchId)
                        print '写入%s' %newMatchId
                        for j in xrange(0,10):
                            if v == l['players'][j]['account_id']:
                                floor = j+1
                                heroId = l['players'][j]['hero_id']
                                break
                        if floor >5:
                            isDirOrRadin = 1 #天灾
                        else:
                            isDirOrRadin = 0 #近卫
                        matchDetail = api.get_match_details(matchId)
                        isRadinWin = matchDetail['radiant_win']
                        #使用异或(xor)来判断此局胜负.  bool(xxx) != bool(xxx)
                        WinorLoss =  isDirOrRadin !=  isRadinWin
                        if WinorLoss:
                            flag = 1
                        else:
                            flag = 0
                        assists = matchDetail['players'][floor-1]['assists']
                        deaths = matchDetail['players'][floor-1]['deaths']
                        denies = matchDetail['players'][floor-1]['denies']
                        heroDamage = matchDetail['players'][floor-1]['hero_damage']
                        kills = matchDetail['players'][floor-1]['kills']
                        lastHits = matchDetail['players'][floor-1]['last_hits']
                        goldSpent = matchDetail['players'][floor-1]['gold_spent']
                        goldPerMin = matchDetail['players'][floor-1]['gold_per_min']
                        xpPerMin = matchDetail['players'][floor-1]['xp_per_min']
                        heroHealing = matchDetail['players'][floor-1]['hero_healing']
                        towerDamage = matchDetail['players'][floor-1]['tower_damage']

                        value = [v,matchId,heroId,floor,flag,assists,denies,deaths,goldPerMin,kills,lastHits,heroDamage,heroHealing,goldSpent,xpPerMin,towerDamage]
                        cursor.execute('INSERT INTO accountPlayed (accountId,matchId,heroId,floor,winOrLoss,assists,denies,deaths,goldPerMin,kills,lastHits,heroDamage,heroHealing,goldSpent,xpPerMin,towerDamage) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',value)
                        conn.commit()

            lastHistory = matchHistory['matches'][len(matchHistory['matches'])-1]['match_id']
            matchHistory = api.get_match_history(account_id=v,start_at_match_id=lastHistory)
            if lastHistory == matchHistory['matches'][len(matchHistory['matches'])-1]['match_id']:
                break

def f1():
    count = 1
    cursor.execute('select  matchId from matchDetail order by  matchid desc ')
    r1 = cursor.fetchall()
    for matchId in r1:
        detail = api.get_match_details(matchId['matchId'])
        gameMode = detail['game_mode']
        matchId = detail['match_id']
        value = [gameMode,matchId]
        cursor.execute('Update matchDetail set gameMode = %s where matchId = %s',value)
        conn.commit()
        count = count + 1
        print count


def run():
    #hero2DB()
    #account2DB()
    #played2DB()
    writeNewMatch2DB()
    mathcDetail2DB()

if __name__ == "__main__":
    d = api.get_match_details(match_id=3043788702)
    run()