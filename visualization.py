# -*- encoding:utf-8 -*-
import wordcloud
import PIL
from wordcloud import WordCloud
import numpy as np
import sys
import data as d2d
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf-8')
import pandas as pd


#生成最近对队对手昵称的词云图
def worldcloud():
    nickname = d2d.getPlayerNickname()
    strNickName = ','.join(nickname)
    alice_mask = np.array(PIL.Image.open('/Users/zidongceshi/code/mydota2/dota.jpg'))
    wordcloud = WordCloud(font_path='/Users/zidongceshi/code/mydota2/'+'华文细黑.ttf',
                          background_color='white',
                          width=1800,
                          height=800,
                          margin=5,
                          #mask=alice_mask,
                          max_words=2000,
                          max_font_size=60,
                          random_state=42)
    wordcloud = wordcloud.generate(strNickName)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    pass