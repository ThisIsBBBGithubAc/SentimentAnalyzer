from appwrite.client import Client
from appwrite.services.database import Database
from appwrite.query import Query
import time, os, sys

client = Client()

(client
  .set_endpoint('http://8080-appwrite-integrationfor-nf192dig6sr.ws-us44.gitpod.io/v1') # Your API Endpoint
  .set_project('627734fdcdd43864f8e4') # Your project ID
  .set_key('0b5f50ce4841e0f9b831d6756ab6d8ad7f7aeda99e96c9d1d6b2a383a69379c930bac2579163fd3291b3f2f395efeed6661defd7bcf2c67f038ac8ed7fa307ce256d35dfbd31c99ad76f2cebae5b84f7bb6f6aa362065f2f8eb89fae34bc0d657c28250dc56f1c826705d8080e4966e9e2cce555f8681cdc6c4aeae63ab07bdc') # Your secret API key
)

database = Database(client)


def create_collection():
    try:
        response = database.create_collection(
            collection_id='sentiment_collection_bbb',
            name='Sentiment_Collection',
            permission='document',
            read=['role:all'],
            write=['role:all']
        )
        collection_id = response['$id']
        # print(response)

        response = database.create_string_attribute(
            collection_id,
            key='username',
            size=255,
            required=True,
        )
        # print(response)

        response = database.create_string_attribute(
            collection_id,
            key='password',
            size=255,
            required=True,
        )
        # print(response)

        response = database.create_email_attribute(
            collection_id,
            key='email',
            required=True,
            default=""
        )
        # print(response)

        # Wait for attributes to be created
        time.sleep(2)
        response = database.create_index(
            collection_id,
            key='username_email_index',
            type="fulltext",
            attributes=['username', 'email']
        )
        # print(response)
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)



def add_document(data):
    try:
        response = database.create_document(
            "sentiment_collection_bbb",
            document_id='unique()',
            data=data,
            read=['role:all'],
            write=['role:all']
        )
        # print(response)
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)


def delete_document(document_id):
    try:
        response = database.delete_document(
            'sentiment_collection_bbb',
            document_id
        )
        # print(response)
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)


def isUserNameExist(value):
    try:
        results = database.list_documents('sentiment_collection_bbb')
        # results = database.list_documents('sentiment_collection_bbb', [Query.search('username', value)])
        for result in results["documents"]:
            if result["username"] == value:
                return result
        return None
    except Exception as emsg:
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)



create_collection()
# print(isUserNameExist("bbb123"))
