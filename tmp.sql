
针对accountid来查开黑胜率
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

月报
select a.nickname,from_unixtime(md.`startTime`,'%Y-%m') as '月份',count(ap.accountid) as'场次',sum(ap.winorloss) as'赢' from accountplayed as ap join `matchDetail` as md join account as a on ap.matchid = md.matchid and ap.accountid = a.accountid group by from_unixtime(md.`startTime`,'%Y-%m'),ap.accountid,a.nickname order by from_unixtime(md.`startTime`,'%Y-%m') desc

日报
select from_unixtime(md.starttime,'%Y%m%d'),h.nickname,ap.winorloss
from `accountPlayed` as ap join `matchDetail` as md join hero as h
on ap.matchid = md.matchid and h.heroid = ap.heroid
where (from_unixtime(md.starttime,'%Y%m%d') = date_format(now(),'%Y%m%d') -1) and ap.accountid = 169478997
order by md.starttime desc

补刀数
select a.nickName,from_unixtime(md.starttime,'%Y%m%d'),ap.accountId,sum(ap.`lastHits`)
from `matchDetail` as md
join accountPlayed as ap join account as a
on md.`matchId` = ap.matchId and a.`accountId` = ap.`accountid`
group by ap.accountId,a.nickName,from_unixtime(md.starttime,'%Y%m%d')

