from fastapi import Depends, APIRouter, Path, HTTPException, Security
from fastapi.responses import ORJSONResponse
from .schema import ScrapingParameters, ScrapingParametersInternal, UserGivenText, AuthModel
from .scraping import scrape_youtube_comments_with_replies
from .analyser_Transformers import get_all_comments, analyze_comments
import os, sys, shortuuid, re

from transformers import pipeline
import pandas as pd

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .auth import Auth
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request, Form
from decouple import config

from deta import Deta

security = HTTPBearer()
auth_handler = Auth()
router = APIRouter()
templates = Jinja2Templates(directory="templates")


PROJECT_KEY = os.environ.get('PROJECT_KEY')
if PROJECT_KEY is None:
    PROJECT_KEY = config('PROJECT_KEY')

DETA_BASE_NAME = os.environ.get('DETA_BASE_NAME')
if DETA_BASE_NAME is None:
    DETA_BASE_NAME = config('DETA_BASE_NAME')

deta = Deta(PROJECT_KEY) 
db = deta.Base(DETA_BASE_NAME)


@router.get("/", tags=["Sentiment Analysis"], response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
    # return {"message": "Welcome to this Sentiment Analyzer!"}


@router.post('/auth/signup', tags=["Sign Up"])
def SignUp(user_details: AuthModel):
    try:
        results = db.fetch({"username": user_details.username}).items
        # fetch_res = fetch_res.items
        if len(results) != 0:
            return {"username_status": "available", "message": "Username already exist!Try another."}
    
        hashed_password = auth_handler.encode_password(user_details.password)    
        data = {"username" : user_details.username, "password" : hashed_password, "email" : user_details.email}
        db.put(data)
        return data
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."

@router.post('/auth/signin', tags=["Sign In"])
def Signin(user_details: AuthModel):
    try:
        user = db.fetch({"username": user_details.username}).items
        if len(user) == 0:
        # print(user)
            return HTTPException(status_code=401, detail='Invalid username')

        if (not auth_handler.verify_password(user_details.password, user[0]['password'])):
            return HTTPException(status_code=401, detail='Invalid password')

        access_token = auth_handler.encode_token(user[0]['username'])
        refresh_token = auth_handler.encode_refresh_token(user[0]['username'])
        return {'access_token': access_token, 'refresh_token': refresh_token}
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."

@router.get('/auth/refresh_token', tags=["Refresh Token"])
def Refresh_Token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        refresh_token = credentials.credentials
        new_token = auth_handler.refresh_token(refresh_token)
        return {'access_token': new_token}
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."



@router.post('/user/delete', tags=["Delete User (Authentication Required)"])
def Delete_Account(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        username = auth_handler.decode_token(token) # return username
        if username:
            # print(auth_handler.decode_token(token))
            user = db.fetch({"username":username}).items
            if len(user) != 0:
                db.delete(user[0].get("key"))
                return "Account deleted successfully."
            else:
                return "No such user exist!"
        else:
            return "Please sign in delete your account"
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."



# @router.post('/SecretMsg')
# def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
#     token = credentials.credentials
#     if(auth_handler.decode_token(token)):
#         return 'This msg can be read by only authorized users'



@router.post("/analysis/youtubeComments", tags=["Sentiment Analysis On YouTube Comments"], response_class=HTMLResponse)
async def Youtube_Comments(request: Request, youtube_link:str=Form(...), maxComments:int=Form(...), maxCommentReplies:int=Form(...), nextPage_retrive_limit:int=Form(...)):
    try:
        # print(youtube_link)
        # print(maxCommentReplies)
        if not youtube_link.startswith("https://www.youtube.com/watch?v=") or "&list=" in youtube_link:
            return {"message": "Invalid URL. Enter a proper youtube link."}
        else:
            video_id = youtube_link[len("https://www.youtube.com/watch?v="):]
            file_name = str(shortuuid.ShortUUID().random(length=8))
            scrape_youtube_comments_with_replies( video_url = video_id, file_name = file_name, maxComments = maxComments, maxCommentReplies = maxCommentReplies, nextPage_retrive_limit = nextPage_retrive_limit )
            
            all_comments = list(get_all_comments(file_name = file_name))
            sentiment_results, positive, negative, neutral = analyze_comments(all_comments)

            os.remove(file_name+".csv")
            return templates.TemplateResponse("home.html", {"request": request, "data": True, "positive" : positive, "negative" : negative, "neutral" : neutral})
            # return {"Positive" : positive, "Negative" : negative, "Neutral" : neutral}

    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."


@router.post("/analysis/UserGivenText", tags=["Sentiment Analysis On User Given Text"], response_class=HTMLResponse)
async def User_Given_Text(request: Request, text:str = Form(...)):
    try:
        sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)', text)
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
            # print(count)
            count+=1
        positive = results[0].get('Positive')
        negative = results[0].get('Negative')
        neutral = results[0].get('Neutral')
        
        each_sentence_info_list = []
        cnt = 0
        for result in results[1:]:
            if cnt == 8:
                break
            each_sentence_info_list.append(result)
            # print(result)
            cnt+=1

        return templates.TemplateResponse("home.html", {"request": request, "each_sentence_info": True, "each_sentence_info_list": each_sentence_info_list, "data": True, "positive" : positive, "negative" : negative, "neutral" : neutral})
        # return {"message" : results}
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."
    



@router.post("/api/analysis/youtubeComments", tags=["Sentiment Analysis On YouTube Comments (Authentication Required)"])
async def Youtube_Comments(sp : ScrapingParameters, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
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
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."


@router.post("/api/analysis/UserGivenText", tags=["Sentiment Analysis On User Given Text (Authentication Required)"])
async def User_Given_Text(text:UserGivenText, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        text = dict(text)
        sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)', text.get('user_given_text'))
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
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)
        return "Something went wrong! Try later."
