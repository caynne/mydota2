# -*- encoding:utf-8 -*-
import data as d2d
import json
import codecs
import sys
import PIL
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from configparser import ConfigParser
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

cf = ConfigParser()
cf.read('config.conf')
friden = {'ass':cf.getint('constant','ass'),'bear':cf.getint('constant','bear'),'brave':cf.getint('constant','brave'),'monkey1':cf.getint('constant','monkey1'),'man':cf.getint('constant','man'),'beard':cf.getint('constant','beard')}

poolList = d2d.getHeroPool(friden['beard'])

data = pd.Series(poolList)

print data

if __name__ == "__main__":
    pass
