from operator import neg
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re, sys, os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


def clean_text(comment):
    '''
    Utility function to clean comment text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", comment).split())
  
def get_text_sentiment(comment):
    
    '''
    Utility function to classify sentiment of passed comment
    using textblob's sentiment method
    '''
    # create TextBlob object of passed comment text
    analysis = TextBlob(clean_text(comment))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

pve = {}
pvelist = []
nve = {}
nvelist = []
neu = {}
neulist = []
all_comments = []


def get_all_comments(file_name='abc'):
    data = pd.read_csv(f'{file_name}.csv', lineterminator='\n')
    data.head()
    data['Comment'] = data['Comment'].to_string().replace('[^\w]',' ')
    return data['Comment']

all_comments = get_all_comments()

def analyze(all_comments = all_comments):
    
    for cmnt in all_comments:
        sentiment = get_text_sentiment(cmnt)
        if sentiment == 'positive':
            pve["comment"] = cmnt
            pve["sentiment"] = sentiment
            pvelist.append(cmnt)
        
        if sentiment == 'negative':
            nve["comment"] = cmnt
            nve["sentiment"] = sentiment
            nvelist.append(cmnt)

        if sentiment == 'neutral':
            neu["comment"] = cmnt
            neu["sentiment"] = sentiment
            neulist.append(cmnt)

# analyze()

# print("Positive Comments: {} %".format(100*len(pvelist)/len(all_comments)))

# print("Negative Comments: {} %".format(100*len(nvelist)/len(all_comments)))

# print("Neutral Comments: {} %".format(100*len(neulist)/len(all_comments)))

# print(pvelist[:3])
