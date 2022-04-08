from pymongo import MongoClient
import json
from pathlib import Path
import os


db_client = MongoClient(
    host="127.0.0.1",
    port=27017,
    username="root",
    password="example",
)

data_path = Path("scripts/plant_data_08_04_2022.json")


dbs = ["dev", "test"]

for db_name in dbs:
    db = db_client[db_name]
    plants_collection = db["plants"]
    plants_collection.drop()
    with open(data_path) as file:
        file_data = json.load(file)

    plants_collection.insert_many(file_data)

# * upload to cloud test env

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "test")

if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    plants_collection = db["plants"]
    plants_collection.drop()
    with open(data_path) as file:
        file_data = json.load(file)

    plants_collection.insert_many(file_data)
else:
    print("No MONGO_URI env variable found")
