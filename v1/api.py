from fastapi import Depends, APIRouter, Path, HTTPException, Security
from fastapi.responses import ORJSONResponse
from .schema import ScrapingParameters, ScrapingParametersInternal
from .scraping import scrape_youtube_comments_with_replies
from .analyser_Transformers import get_all_comments, analyze_comments
import os, sys, shortuuid, re

from transformers import pipeline
import pandas as pd

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .auth import Auth
from .schema import AuthModel


security = HTTPBearer()
auth_handler = Auth()
router = APIRouter()




@router.get("/")
async def read_root():
    return {"message": "Welcome to this app!"}





@router.post('/signup')
def signup(user_details: AuthModel):
    
    if users_db.get(user_details.username) != None:
        return 'Account already exists'
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        user = {'key': user_details.username, 'password': hashed_password}
        users_db = user.copy()
        return users_db
    except:
        error_msg = 'Failed to signup user'
        return error_msg

@router.post('/login')
def login(user_details: AuthModel):
    user = users_db.get(user_details.username)
    if (user is None):
        return HTTPException(status_code=401, detail='Invalid username')
    if (not auth_handler.verify_password(user_details.password, user['password'])):
        return HTTPException(status_code=401, detail='Invalid password')

    access_token = auth_handler.encode_token(user['key'])
    refresh_token = auth_handler.encode_refresh_token(user['key'])
    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

@router.post('/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@router.get('/notsecret')
def not_secret_data():
    return 'Not secret data'





@router.post("/analyse/youtubeComments")
async def read_root(sp : ScrapingParameters):
    sp = dict(sp)
    file_name = str(shortuuid.ShortUUID().random(length=8))
    spi = ScrapingParametersInternal(video_url = sp.get("video_url"), file_name = file_name, maxComments = sp.get("maxComments"), maxCommentReplies = sp.get("maxCommentReplies"), nextPage_retrive_limit = sp.get("nextPage_retrive_limit"))
    spi = dict(spi)
    if spi.get("video_url") == "InvalidURL":
        return {"message": "Invalid URL. Enter a proper youtube URL."}
    scrape_youtube_comments_with_replies(video_url = spi.get("video_url"), file_name = file_name, maxComments = spi.get("maxComments"), maxCommentReplies = spi.get("maxCommentReplies"), nextPage_retrive_limit = spi.get("nextPage_retrive_limit"))
    
    all_comments = list(get_all_comments(file_name = file_name))
    positive, negative, neutral = analyze_comments(all_comments)

    os.remove(file_name+".csv")
    return {"Positive" : positive, "Negative" : negative, "Nuetral" : neutral}

@router.get("/analyse/CustomText/{text}")
async def customText(text : str= Path(None, title="Add text to analise the sentiment of those text")):

    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)
    for s in sentences:
        if s == ' ':
            sentences.remove(' ')

    # print(type(sentences))
    # print(sentences)

    
    sentiment_results, positive, negative, neutral = analyze_comments(sentences)
    count = 0
    results = []
    sentiment_total = {"Positive" : positive, "Negative" : negative, "Neutral" : neutral}
    results.append(sentiment_total)
     
    for sentence in sentences:
        result = {}
        result["sentence"] = sentence
        result["sentiment"] = sentiment_results[count]["label"]
        result["score"] = sentiment_results[count]["score"]
        results.append(result)
        print(count)
        count+=1

    return {"message" : results}
    
