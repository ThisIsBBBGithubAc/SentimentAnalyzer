from transformers import pipeline
import pandas as pd

sentiment_pipeline = pipeline("sentiment-analysis")

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

sentiment_pipeline(all_comments)


# print("Positive Comments: {} %".format(100*len(pvelist)/len(all_comments)))

# print("Negative Comments: {} %".format(100*len(nvelist)/len(all_comments)))

# print("Neutral Comments: {} %".format(100*len(neulist)/len(all_comments)))

