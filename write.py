#!/usr/bin/env python
# encoding=utf-8

import data as d2d
import xlwt
import json
import codecs
import sys

reload(sys)
sys.getdefaultencoding()

friden = {"brave":169478997,"bear":337190674,"monkey":131173904,"man":284155258,"beard":245587068,"ass":123343610}

def writeHeroPool2csv():
    #for k,v in friden.items():
    heroPool = d2d.getHeroPool(169478997)
    heroPoolJson = json.dumps(heroPool)
    print heroPool




if __name__ == "__main__":
    writeHeroPool2csv()