from pymongo import MongoClient
import json


db_client = MongoClient(
        host='127.0.0.1',
        port=27017,
        username='root',
        password='example',
    )


dbs = ["dev", "test"]

for db_name in dbs:
    db = db_client[db_name]
    plants_collection = db["plants"]
    plants_collection.drop()
    with open('scripts/plant_data_1_11_2021.json') as file:
        file_data = json.load(file)

    plants_collection.insert_many(file_data)