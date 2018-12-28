from selenium import webdriver
import sys
import numpy as np
from PIL import Image
import nltk as nltk
from nltk import *
import time
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
#nltk.download('averaged_perceptron_tagger')--download if not present 
#nltk.download('punkt')--download if not present

#to get comments from the video
#download the suitable webdriver based on the browser
img_path=input("enter the image path")
video_link=input("enter the link")
driver=webdriver.Firefox()
driver.get(video_link)
driver.execute_script('window.scrollTo(1, 500);')
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

#to load the comments-change the sleep time based on the speed of the internet connection
time.sleep(8)
driver.execute_script('window.scrollTo(1, 3000);')
comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')
comment_list=[]
com_pos=[]
noun_list=[]
for comment in comments:    
    comment_list.append(comment.text.translate(non_bmp_map))
for com in comment_list:
  comm=word_tokenize(com)
  com_pos.append(nltk.pos_tag(comm))
for sentence in com_pos:
    for word in sentence:
        if word[1][0]=='N':
            noun_list.append(word[0])


#mask image for the wordcloud-note: the image should not have any transparent part
#maskk_img=np.array(Image.open(r"/home/hp/Desktop/ralph1.jpg"))-- for windows
            
maskk_img=np.array(Image.open(img_path))
#to generate text based on the colour on the image
maskk_colour=ImageColorGenerator(maskk_img)
text=""
for letter in noun_list:
  text=text+","+letter
wc = WordCloud(width=1000,height=1000,background_color="white",mask=maskk_img,contour_width=5,contour_color='black')
wc.generate(text)

#saving the wordcloud
plt.figure(figsize=(10,10))
plt.imshow(wc.recolor(color_func=maskk_colour), interpolation='bilinear')
plt.axis("off")
plt.savefig("/home/hp/Desktop/ralphword.png",format="png")
plt.show()

