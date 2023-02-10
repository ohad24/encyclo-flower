from pathlib import Path
import json
import boto3
from pprint import pprint
import requests
from io import BytesIO
import os

s3_client = boto3.client('s3')

BUCKET_NAME = 'ef-inaturalist'

# plants = json.loads(Path('plants_count.json').read_text())

# print(len(plants))


# image_url = "https://stimg.cardekho.com/images/carexteriorimages/930x620/Lamborghini/Aventador/6721/Lamborghini-Aventador-SVJ/1621849426405/side-view-(left)-90.jpg"

# res = requests.get(image_url)

# print(res.content)

# client.upload_file(res.content, BUCKET_NAME, '1.jpg')

# os.path.basename("https://example.com/file.html")

# client.upload_fileobj(BytesIO(res.content), BUCKET_NAME, '1.jpg')

# lo = client.list_objects(Bucket=BUCKET_NAME, Prefix='images/').get("Contents")

# for i in lo:
#     print(i.get('Key'))

s3_response_object = s3_client.get_object(
        Bucket=BUCKET_NAME, Key="data/Phytolacca americana.json"
    )
data = json.loads(s3_response_object["Body"].read())