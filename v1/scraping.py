from googleapiclient.discovery import build
import pandas as pd
import sys, os
from decouple import config


developerKey = os.environ.get('GOOGLE_DEVELOPER_KEY')
if developerKey is None:
    developerKey = config('GOOGLE_DEVELOPER_KEY')
    
youtube = build('youtube', 'v3', developerKey=developerKey)

def scrape_youtube_comments_with_replies(video_url, file_name, maxComments, maxCommentReplies, nextPage_retrive_limit, youtube=youtube):


    """The maxResults parameter specifies the maximum number of items that should be returned in the result set.
    Note: This parameter is not supported for use in conjunction with the id parameter. Acceptable values are 1 to 100, inclusive. The default value is 20."""


    try:
        data = youtube.commentThreads().list(part='snippet', videoId=video_url, maxResults=maxComments, textFormat="plainText").execute()
        box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]

        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']
            
            box.append([name, comment, published_at, likes, replies])
            
            totalReplyCount = i["snippet"]['totalReplyCount']
            
            if totalReplyCount > 0:
                
                parent = i["snippet"]['topLevelComment']["id"]
                
                data2 = youtube.comments().list(part='snippet', maxResults=maxCommentReplies, parentId=parent,
                                            textFormat="plainText").execute()
                
                for i in data2["items"]:
                    name = i["snippet"]["authorDisplayName"]
                    comment = i["snippet"]["textDisplay"]
                    published_at = i["snippet"]['publishedAt']
                    likes = i["snippet"]['likeCount']
                    replies = ""

                    box.append([name, comment, published_at, likes, replies])

        nextPage_retrive_count = 0
        while ("nextPageToken" in data):

            if nextPage_retrive_count > nextPage_retrive_limit:
                print(nextPage_retrive_count)
                break
            
            data = youtube.commentThreads().list(part='snippet', videoId=video_url, pageToken=data["nextPageToken"],
                                             maxResults=maxComments, textFormat="plainText").execute()
                                             
            for i in data["items"]:
                name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
                likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
                replies = i["snippet"]['totalReplyCount']

                box.append([name, comment, published_at, likes, replies])

                totalReplyCount = i["snippet"]['totalReplyCount']

                if totalReplyCount > 0:
                    
                    parent = i["snippet"]['topLevelComment']["id"]

                    data2 = youtube.comments().list(part='snippet', maxResults=maxCommentReplies, parentId=parent, textFormat="plainText").execute()

                    for i in data2["items"]:
                        name = i["snippet"]["authorDisplayName"]
                        comment = i["snippet"]["textDisplay"]
                        published_at = i["snippet"]['publishedAt']
                        likes = i["snippet"]['likeCount']
                        replies = ''

                        box.append([name, comment, published_at, likes, replies])

            nextPage_retrive_count+=1


        df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                       'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})
        
        sql_vids = pd.DataFrame([])

        sql_vids = sql_vids.append(df) # pip install pandas==1.3
        
        
        sql_vids.to_csv(f'{file_name}.csv', index=False, header=False)

    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)


# scrape_youtube_comments_with_replies(video_url="7S_tz1z_5bA", file_name="abc", maxComments=10, maxCommentReplies=1, nextPage_retrive_limit=1)

