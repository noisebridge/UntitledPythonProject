# Script to insert movies and interactions into MongoDB

from dotenv import load_dotenv
import os
import pymongo
from pymongo import MongoClient

load_dotenv()

def insert_into_mongo(data):
    db_username = os.getenv('mongodb_username')
    db_password = os.getenv('mongodb_password')

    mongo_url = os.getenv('mongodb_uri')
    client = MongoClient(mongo_url, username = db_username, password = db_password)
    db = client['mediabridge']
    collection = db["movies"]

    for movie in data:
        collection.update_one({'wikidata_id': movie[1]},
            {'$set': {
             'netflix_id': movie[0],
             'wikidata_id': movie[1],
             'title': movie[2], 
             'year': movie[3],
             'genre': movie[4],
             'director': movie[5]} },
             upsert = True)

    print(f'Mongo DB entries: {collection.count_documents({})}')





