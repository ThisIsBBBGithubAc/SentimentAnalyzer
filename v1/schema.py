from typing import Optional
from pydantic import BaseModel, EmailStr, AnyHttpUrl, validator, Field


class ScrapingParameters(BaseModel):
    video_url : AnyHttpUrl
    maxComments : Optional[int] = Field(20, gt =0, le = 100, description="Maximum comments to be returned")
    maxCommentReplies : Optional[int] = Field(20, gt =0, le = 100, description="Maximum comment's replies to be returned")
    nextPage_retrive_limit : Optional[int] = Field(20, gt =0, le = 100, description="Number of available next page's comments to returned")
    
    

class ScrapingParametersInternal(ScrapingParameters):
    file_name : Optional[str] = Field(..., title="This file name is in WordCloud image", max_length=8)

    @validator('video_url')
    def verify_link(cls, v):
        if not v.startswith("https://www.youtube.com/watch?v=") or "&list=" in v:
            # raise ValueError('Invalid URL. Enter a proper youtube URL.')
            return "InvalidURL"
        return v[len("https://www.youtube.com/watch?v="):]
    
class UserGivenText(BaseModel):
    user_given_text: str

class AuthModel(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None