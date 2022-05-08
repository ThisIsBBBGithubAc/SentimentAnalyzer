from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re, sys, os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


def analyse_comments(file_name):
    try:
        data = pd.read_csv(f'{file_name}.csv', lineterminator='\n')
        data.head()

        data['Comment'] = data['Comment'].to_string().replace('[^\w]',' ')


        def getSubjectivity(text):
            return TextBlob(text).sentiment.subjectivity

        data['Subjectivity'] = data['Comment'].apply(getSubjectivity)



        def getPolarity(text):
            return TextBlob(text).sentiment.polarity

        data['Polarity'] = data['Comment'].apply(getPolarity)



        # allWords = ' '.join( [cmts for cmts in data['Comment']])
        # wordCloud = WordCloud(width = 500, height = 300, random_state = 21, max_font_size = 119).generate(allWords)

        # plt.imshow(wordCloud, interpolation= 'bilinear')
        # plt.axis('off')
        # plt.show
        # plt.savefig(f'{file_name}.png')


        def getAnalysis(score):
            if score < 0 :
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'

        data['Analysis'] = data['Polarity'].apply(getAnalysis)



        pcomments = data[data.Analysis == 'Positive']
        pcomments = pcomments['Comment']
        positive = round((pcomments.shape[0]/data.shape[0])*100, 1)
        positive_percentage = str(positive)+ '%'
        print('Positive: ' + positive_percentage)
        # pcomments = list(pcomments)
        # print(pcomments[:1])

        ncomments = data[data.Analysis == 'Negative']
        ncomments = ncomments['Comment']
        negative = round((ncomments.shape[0]/data.shape[0])*100, 1)
        negative_percentage = str(negative)+ '%'
        print('Negative: ' + negative_percentage)


        neucomments = data[data.Analysis == 'Neutral']
        neucomments = neucomments['Comment']
        neutral = round((neucomments.shape[0]/data.shape[0])*100, 1)
        neutral_percentage = str(neutral)+ '%'
        print('neutral: ' + neutral_percentage)



        # data['Analysis'].value_counts

        # plt.title('Sentiment Analysis')
        # plt.xlabel('Sentiment')
        # plt.ylabel('Counts')
        # data['Analysis'].value_counts().plot(kind= 'pie')
        # plt.show()
        # plt.savefig('my_plot.png')

        # sentiment = None
        # if positive > neutral:
        #     sentiment = positive
        # else:
        #     sentiment = neutral
        # if sentiment < negative:
        #     sentiment = negative


        return (positive_percentage, negative_percentage, neutral_percentage)
    
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)


# analyse_comments(file_name = "abc")

