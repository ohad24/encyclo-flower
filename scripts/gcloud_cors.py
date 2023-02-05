import sys

# from dotenv import load_dotenv
import os

# google GOOGLE_APPLICATION_CREDENTIALS env variable
os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/home/ohadm/projects/encyclo-flower/src/api/google_cred.json"

# load_dotenv('src/api/.env')

# [START storage_cors_configuration]
from google.cloud import storage


def cors_configuration(bucket_name):
    """Set a bucket's CORS policies configuration."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.cors = [
        {
            "origin": ["*"],
            "responseHeader": ["Content-Type", "x-goog-resumable"],
            "method": ["GET"],
            "maxAgeSeconds": 3600,
        }
    ]
    bucket.patch()

    print(f"Set CORS policies for bucket {bucket.name} is {bucket.cors}")
    return bucket


# [END storage_cors_configuration]

if __name__ == "__main__":
    cors_configuration(bucket_name=sys.argv[1])
