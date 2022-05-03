from fastapi import Depends, APIRouter
from fastapi.responses import ORJSONResponse
from .schema import ScrapingParameters, ScrapingParametersInternal
from .scraping import scrape_youtube_comments_with_replies
from .analyser import analyse_comments
import os, sys, shortuuid

from transformers import pipeline
import pandas as pd


router = APIRouter()



@router.get("/")
async def read_root():
    return {"message": "Welcome to this app!"}

@router.post("/analyse/youtubeComments")
async def read_root(sp : ScrapingParameters):
    sp = dict(sp)
    file_name = str(shortuuid.ShortUUID().random(length=8))
    spi = ScrapingParametersInternal(video_url = sp.get("video_url"), file_name = file_name, maxComments = sp.get("maxComments"), maxCommentReplies = sp.get("maxCommentReplies"), nextPage_retrive_limit = sp.get("nextPage_retrive_limit"))
    spi = dict(spi)
    if spi.get("video_url") == "InvalidURL":
        return {"message": "Invalid URL. Enter a proper youtube URL."}
    scrape_youtube_comments_with_replies(video_url = spi.get("video_url"), file_name = file_name, maxComments = spi.get("maxComments"), maxCommentReplies = spi.get("maxCommentReplies"), nextPage_retrive_limit = spi.get("nextPage_retrive_limit"))
    positive , negative, nuetral, sentiment = analyse_comments(file_name = file_name)
    os.remove(file_name+".csv")
    return {"Positive" : positive, "Negative" : negative, "Nuetral" : nuetral, "Sentiment" : sentiment}

@router.get("/analyse/CustomText")
async def read_root(sp : ScrapingParameters):
    sentiment_pipeline = pipeline("sentiment-analysis")
    data = ["I love you", "I hate you"]
    sentiment_pipeline(data)