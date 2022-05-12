import uvicorn
from fastapi import FastAPI
from v1 import api
from fastapi.middleware.cors import CORSMiddleware

description = """

**This API enables developers to use the json data of Sentiment Analysis of YouTube comments and user given text
🚀**

  
  

## **Features**

  - Developer first need to signup to user this API
  - This API returns json data of sentiment of YouTube comments and user given text
  - Users can use this API without authentication to perform sentiment analysis on
    YouTube comments and user given text. JSON data will be returned only after authentication

  

"""

tags_metadata = [

    {
        "name": "Sentiment Analysis",
        "description": "Hello, this is a sentiment analyser REST API."
    },

    {
        "name": "Sign Up",
        "description": "This endpoint is for registering users to use this API data"
    },

    {
        "name": "Sign In",
        "description": "This endpoint is for authentication."
    },
    {
        "name": "Refresh Token",
        "description": "This endpoint receives a refresh token which is then passed onto the the function from auth logic to get a new token."
    },
    {
        "name": "Delete User (Authentication Required)",
        "description": "This endpoint is for deleting user data completely."
    },
    {
        "name": "Sentiment Analysis On YouTube Comments",
        "description": "This endpoint performs sentiment analysis on YouTube comments."
    },
    
    {
        "name": "Sentiment Analysis On User Given Text",
        "description": "This endpoint performs sentiment analysis on user given text."
    },

    {
        "name": "Sentiment Analysis On YouTube Comments (Authentication Required)",
        "description": "This endpoint returns json data of sentiment analysis on YouTube comments."
    },

    {
        "name": "Sentiment Analysis On User Given Text (Authentication Required)",
        "description": "This endpoint returns json data of sentiment analysis on user given text."
    },


]


app = FastAPI(

    docs_url="/doc",
    redoc_url=None,
    title="REST API For Sentiment Analysis",
    description=description,
    version="0.0.1",
    # terms_of_service="http://bbbwebsite.com/terms/",
    contact={
        "name": "Developer",
        # "url": "https://bbbwebsite.com/contact/",
        "email": "imax7964@gmail.com",
    },
    license_info={
        "name": "The MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata

    )

app.include_router(api.router)

# origins = [
#     "http://127.0.0.1:8000",
#     "https://8000-appwrite-integrationfor-nf192dig6sr.ws-us44.gitpod.io/",
# ]

origins = ["*"] # not recommended for production

# "In order for our REST API endpoints to be consumed in client applications such as Vue, React, Angular or any other Web applications that are running on other domains, we should tell our FastAPI to allow requests from the external callers to the endpoints of this FastAPI application. We can enable CORS (Cross Origin Resource Sharing) either at application level or at specific endpoint level."
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


#used for development environment
if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
