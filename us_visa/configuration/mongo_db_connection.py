import sys
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)
     # Searches parent directories automatically
from us_visa.exception import USvisaException
from us_visa.logger import logging

from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY
import pymongo
import certifi
from typing import ClassVar, Optional

ca = certifi.where()

class MongoDBClient:
    """
    Class Name :   export_data_into_feature_store
    Description :   This method exports the dataframe from mongodb feature store as dataframe 
    
    Output      :   connection to mongodb database
    On Failure  :   raises an exception
    """
    client: ClassVar[Optional[pymongo.MongoClient]] = None  # type: ignore[assignment]

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client: pymongo.MongoClient = MongoDBClient.client  # type: ignore[assignment]
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection succesfully established.")
        except Exception as e:
            raise USvisaException(e,sys)