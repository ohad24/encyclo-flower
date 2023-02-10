from pathlib import Path
import json
import boto3
from pprint import pprint
import requests
from io import BytesIO
import os
import csv

s3_client = boto3.client('s3')

BUCKET_NAME = 'ef-inaturalist'

BUCKET_PATH = 'data/'



def get_plants_link(obj, plant_name):
    # get blob from s3
    blob = s3_client.get_object(Bucket=BUCKET_NAME, Key=obj.get("Key"))
    data = json.loads(blob['Body'].read())
    links = []
    for observation in data["observations"]:
        # print(observation['observation_data']['references'])
        for media in observation["medias"]:
            links.append(media["identifier"])
    return links


def write_csv(links, plant_name):
    with open('plants_links.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['plant_name', 'link'])
        for link in links:
            writer.writerow([plant_name, link])

s3 = boto3.client('s3')
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=BUCKET_PATH)
for i, page in enumerate(pages):
    # print(len(page["Contents"]))
    for j, obj in enumerate(page['Contents']):
        plant_name = obj.get("Key")[5:-5]
        links = get_plants_link(obj, plant_name)
        # print(links)
        write_csv(links, plant_name)
        print(i, j)
