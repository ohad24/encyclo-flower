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
    with open('scripts/plant_data_31_01_2022.json') as file:
        file_data = json.load(file)

    plants_collection.insert_many(file_data)

    # plants_collection = db["images"]
    # plants_collection.drop()
    # with open('scripts/plant_data_27_11_2021_images.json') as file:
    #     file_data = json.load(file)

    # plants_collection.insert_many(file_data)
