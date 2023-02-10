from pathlib import Path
import json

import boto3
from pprint import pprint
import requests
from io import BytesIO
import os
from multiprocessing import Pool
from time import sleep


# s3_client = boto3.client("s3")
BUCKET_NAME = "ef-inaturalist"

NUM_OF_PLANTS = -1
NUM_OF_IMAGES = 1000
NUM_OF_PROCESSES = 16


def data_amount_filter():
    s3_client = boto3.client("s3")
    plants_data = []
    s3_response_object = s3_client.get_object(
        Bucket=BUCKET_NAME, Key="plants_count.json"
    )
    plants_count_data = json.loads(s3_response_object["Body"].read())

    for plant in plants_count_data:
        # if plant["count"] > NUM_OF_IMAGES:
        if plant["count"] > 0:
            plants_data.append(plant)
            if len(plants_data) == NUM_OF_PLANTS:
                break
    return plants_data


def setup_urls(plant):
    s3_client = boto3.client("s3")
    # for idx, plant in enumerate(plants_data):
    # plant_name = plant['plant']
    # print(plant["plant"])
    plant_location = plant["location"].replace("inaturalist/", "")
    # blob = bucket.blob(plant_location)
    # data = json.loads(blob.download_as_string())
    # try:
    s3_response_object = s3_client.get_object(Bucket=BUCKET_NAME, Key=plant_location)
    data = json.loads(s3_response_object["Body"].read())
    # except Exception as e:
    # print(e)
    print("aaaa", plant["plant"], len(data["observations"]))
    # return
    # print(data)
    links = []
    for observation in data["observations"]:
        # print(observation['observation_data']['references'])
        for media in observation["medias"]:
            url = media["identifier"]
            catalog_number = media["catalogNumber"]
            links.append({"url": url, "catalog_number": catalog_number})
            # plants_data[idx]["links"] = links
            plant["links"] = links
            if len(links) == NUM_OF_IMAGES:
                break
        if len(links) == NUM_OF_IMAGES:
            break
    return plant


def download_images(plant):
    # if not plant:
    #     return


    s3_client = boto3.client("s3")
    s3_objects = s3_client.list_objects(
        Bucket=BUCKET_NAME, Prefix=f'images/{plant["plant"]}/'
    ).get("Contents")

    # if not s3_objects:
    #     print(plant["plant"], s3_objects)
    #     return
    current_catalog_numbers = (
        [x.get("Key").split("/")[-1].split(".")[0] for x in s3_objects]
        if s3_objects
        else []
    )
    
    print("downlaod images existed", len(current_catalog_numbers))
    
    # print(current_catalog_numbers)
    for link in plant.get("links", None):
        # print(link['catalog_number'], current_catalog_numbers)
        if Path("./stop").is_file():
            print("stop by user")
            break
        if str(link["catalog_number"]) in current_catalog_numbers:
            print(f'{link["catalog_number"]} already exists')
            continue
        try:
            r = requests.get(link["url"], stream=True)
            # print(r.status_code)
            file_path = f'images/{plant["plant"]}/{link["catalog_number"]}.{link["url"].split(".")[-1]}'
            # # print(file_path)
            # image_blob = bucket.blob(file_path)
            # image_blob.upload_from_string(
            #     r.content, content_type=r.headers["content-type"]
            # )
            s3_client.upload_fileobj(
                BytesIO(r.content),
                BUCKET_NAME,
                file_path,
            )
        except Exception as e:
            print(e)
    sleep(1)


if "__main__" == __name__:
    # plants = read_plants_count()
    # print(len(plants))
    # plants = [plants[0]]  # ! remove this line to download all images
    # for plant in plants:
    #     print(plant)
    #     plant_file_name = plant.get('location').replace('inaturalist/', '')
    #     print(plant_file_name)
    #     with open(plant_file_name, 'r') as f:
    #         plant_data = json.load(f)
    #     print(len(plant_data))

    plants_data = plants_data_filtered = data_amount_filter()
    print(len(plants_data_filtered))
    with Pool(NUM_OF_PROCESSES) as p:
        # plants_data_with_urls = setup_urls(plants_data_filtered)
        plants_data_with_urls = p.map(setup_urls, plants_data_filtered)
    print(1)
    with Pool(NUM_OF_PROCESSES) as p:
        p.map(download_images, plants_data_with_urls)
