from pymongo import MongoClient
import json


db_client = MongoClient(
        host='127.0.0.1',
        port=27017,
        username='root',
        password='example',
    )

db = db_client['dev']

plants_collection = db["plants"]
  

with open('scripts/plants_data.json') as file:
    file_data = json.load(file)

plants_collection.insert_many(file_data)