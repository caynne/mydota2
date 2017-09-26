select how1,sum(how2)
from(select ap2.accountid as how1,ap1.`winOrLoss` as how2
from `accountPlayed` as ap1  join matchDetail as md join accountplayed as ap2
on ap1.matchid = md.matchid and ap1.matchid = ap2.matchid
where md.`startTime`> UNIX_TIMESTAMP('2017-03-06-12') and ap2.accountid = 169478997
group by ap1.matchid,ap1.`winOrLoss`
having count(ap1.matchid) > 0) as t1
group by how1

#查看小黑屋及胜场
select a.nickname,count(*) as '场次',sum(winorloss)'胜场'
from accountplayed as ap join matchdetail as md join account as a
on ap.matchid = md.matchid and a.accountid = ap.accountid
where md.`gameMode` = 4
group by ap.accountid,a.nickname
order by count(*) desc




按xx周\用户分组，查询每周数据
select a.nickName,
sum(CASE week(from_unixtime(md.startTime)) WHEN 12 THEN 1 ELSE 0 END )as '第十二周',
sum(CASE week(from_unixtime(md.startTime)) WHEN 13 THEN 1 ELSE 0 END )as '第十三周',
sum(CASE week(from_unixtime(md.startTime)) WHEN 14 THEN 1 Else 0 END) as '第十四周',
sum(CASE week(from_unixtime(md.startTime)) WHEN 15 THEN 1 Else 0 END) as  '第十五周',
sum(CASE week(from_unixtime(md.startTime)) WHEN 16 THEN 1 Else 0 END) as '第十六周 '
from accountplayed as ap join matchdetail as md join account as a
on md.matchId = ap.matchId and a.accountId = ap.accountId
where date_format(from_unixtime(md.startTime),'%Y%m') >=201703
group by ap.accountId,a.nickName

#月操作盘数
SELECT  DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") AS '时间',
	COUNT(CASE WHEN ap.accountId = 169478997 THEN ap.accountId END) AS '勇敢',
	COUNT(CASE WHEN ap.accountId = 337190674 THEN ap.accountId END) AS '胖子',
	COUNT(CASE WHEN ap.accountId = 131173904 THEN ap.accountId END) AS '猴一',
	COUNT(CASE WHEN ap.accountId = 284155258 THEN ap.accountId END) AS '男神',
	COUNT(CASE WHEN ap.accountId = 245587068 THEN ap.accountId END) AS '胡子',
	COUNT(CASE WHEN ap.accountId = 336778995 THEN ap.accountId END) AS '猴二'
FROM accountplayed AS ap
JOIN account AS a ON ap.`accountId` = a.`accountId`
JOIN matchdetail AS md ON md.`matchId` = ap.`matchId`
WHERE DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") > 201609
GROUP BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m")
ORDER BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") DESC;
#月胜率
SELECT  DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") AS '时间',
	ROUND(SUM(CASE WHEN ap.accountId = 169478997 THEN ap.`winOrLoss`  END)/COUNT(CASE WHEN ap.accountId = 169478997 THEN ap.accountId END),2) AS '勇敢',
	ROUND(SUM(CASE WHEN ap.accountId = 337190674 THEN ap.`winOrLoss`  END)/COUNT(CASE WHEN ap.accountId = 337190674 THEN ap.accountId END),2) AS '胖子',
	ROUND(SUM(CASE WHEN ap.accountId = 131173904 THEN ap.`winOrLoss`  END)/COUNT(CASE WHEN ap.accountId = 131173904 THEN ap.accountId END),2) AS '猴一',
	ROUND(SUM(CASE WHEN ap.accountId = 284155258 THEN ap.`winOrLoss`  END)/COUNT(CASE WHEN ap.accountId = 284155258 THEN ap.accountId END),2) AS '男神',
	ROUND(SUM(CASE WHEN ap.accountId = 245587068 THEN ap.`winOrLoss`  END)/COUNT(CASE WHEN ap.accountId = 245587068 THEN ap.accountId END),2) AS '胡子',
	ROUND(SUM(CASE WHEN ap.accountId = 336778995 THEN ap.`winOrLoss`  END)/COUNT(CASE WHEN ap.accountId = 336778995 THEN ap.accountId END),2) AS '猴二'

FROM accountplayed AS ap
JOIN account AS a ON ap.`accountId` = a.`accountId`
JOIN matchdetail AS md ON md.`matchId` = ap.`matchId`
WHERE DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") > 201609
GROUP BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m")
ORDER BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") DESC;
#月操刀英雄数
SELECT  DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") AS '时间',
	COUNT(DISTINCT CASE WHEN ap.accountId = 169478997 THEN ap.`heroId` END) AS '勇敢',
	COUNT(DISTINCT CASE WHEN ap.accountId = 337190674 THEN ap.`heroId` END) AS '胖子',
	COUNT(DISTINCT CASE WHEN ap.accountId = 131173904 THEN ap.heroId END) AS '猴一',
	COUNT(DISTINCT CASE WHEN ap.accountId = 284155258 THEN ap.heroId END) AS '男神',
	COUNT(DISTINCT CASE WHEN ap.accountId = 245587068 THEN ap.heroId END) AS '胡子',
	COUNT(DISTINCT CASE WHEN ap.accountId = 336778995 THEN ap.heroId END) AS '猴二'
FROM accountplayed AS ap
JOIN account AS a ON ap.`accountId` = a.`accountId`
JOIN matchdetail AS md ON md.`matchId` = ap.`matchId`
WHERE DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") > 201609
GROUP BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m")
ORDER BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") DESC;
#月游戏时长
SELECT  DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") AS '时间(游戏时长/分钟)',
	SUM( CASE WHEN ap.accountId = 169478997 THEN md.`duration` ELSE 0 END) AS '勇敢',
	SUM( CASE WHEN ap.accountId = 337190674 THEN md.`duration` ELSE 0 END) AS '胖子',
	SUM( CASE WHEN ap.accountId = 131173904 THEN md.`duration` ELSE 0 END) AS '猴一',
	SUM( CASE WHEN ap.accountId = 284155258 THEN md.`duration` ELSE 0 END) AS '男神',
	SUM( CASE WHEN ap.accountId = 245587068 THEN md.`duration` ELSE 0 END) AS '胡子',
	SUM( CASE WHEN ap.accountId = 336778995 THEN md.`duration` ELSE 0 END) AS '猴二'
FROM accountplayed AS ap
JOIN account AS a ON ap.`accountId` = a.`accountId`
JOIN matchdetail AS md ON md.`matchId` = ap.`matchId`
WHERE DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") > 201609
GROUP BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m")
ORDER BY DATE_FORMAT(FROM_UNIXTIME(md.`startTime`),"%Y%m") DESC;

