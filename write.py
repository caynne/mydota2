#!/usr/bin/env python
# encoding=utf-8

import data as d2d
import xlwt
import json
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

friden = {"brave":169478997,"bear":337190674,"monkey":131173904,"man":284155258,"beard":245587068,"ass":123343610}

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
    wb.save('heroPool.csv')


if __name__ == "__main__":
    writeHeroPool2csv()