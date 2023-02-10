from genericpath import exists
from pathlib import Path
import requests
import json
from pprint import pprint
import os
from google.cloud import storage
from pathlib import Path
from multiprocessing import Pool
from time import sleep


NUM_OF_PLANTS = 100
NUM_OF_IMAGES = 1000
NUM_OF_PROCESSES = 10



if os.uname()[1] == 'DESKTOP-V31P557':
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"
    ] = "/home/ohad/tests/inatualist/google_cred.json"


storage_client = storage.Client()

bucket = storage_client.get_bucket("plants_ml_data")


def data_amount_filter():
    plants_data = []

    blob = bucket.blob("inaturalist/plants_count.json")
    plants_count_data = json.loads(blob.download_as_bytes())

    # plants_count_data = plants_count_data[::-1]
    for plant in plants_count_data:
        if plant["count"] > NUM_OF_IMAGES:
            plants_data.append(plant)
            if len(plants_data) == NUM_OF_PLANTS:
                break
    return plants_data


# print(plants_data)


def setup_urls(plants_data):
    for idx, plant in enumerate(plants_data):
        # plant_name = plant['plant']
        plant_location = plant["location"]
        blob = bucket.blob(plant_location)
        data = json.loads(blob.download_as_string())
        # print(data)
        links = []
        for observation in data["observations"]:
            # print(observation['observation_data']['references'])
            for media in observation["medias"]:
                url = media["identifier"]
                catalog_number = media["catalogNumber"]
                links.append({"url": url, "catalog_number": catalog_number})
                plants_data[idx]["links"] = links
                if len(links) == NUM_OF_IMAGES:
                    break
            if len(links) == NUM_OF_IMAGES:
                break
    return plants_data


# pprint(plants_data)

# for plant in plants_data:
def download_images(plant):
    print(plant["plant"])
    storage_client = storage.Client()

    bucket = storage_client.get_bucket("plants_ml_data")
    current_images_files_blobs = storage_client.list_blobs(
        bucket, prefix=f'inaturalist/images/{plant["plant"]}'
    )
    # print(list(current_images_files_blobs)[0].md5_hash)
    # quit()
    current_catalog_numbers = [
        x.name.split("/")[-1].split(".")[0] for x in current_images_files_blobs
    ]
    for link in plant["links"]:
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
            file_path = f'inaturalist/images/{plant["plant"]}/{link["catalog_number"]}.{link["url"].split(".")[-1]}'
            # print(file_path)
            image_blob = bucket.blob(file_path)
            image_blob.upload_from_string(
                r.content, content_type=r.headers["content-type"]
            )
        except Exception as e:
            print(e)
    sleep(1)


if __name__ == "__main__":
    plants_data_filtered = data_amount_filter()
    plants_data_with_urls = setup_urls(plants_data_filtered)
    with Pool(NUM_OF_PROCESSES) as p:
        p.map(download_images, plants_data_with_urls)
