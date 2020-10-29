from google.cloud import vision
from urllib.request import urlopen
import io
import logging
import os
import cloudstorage as gcs
from PIL import Image
from google.cloud import storage
import requests
import tweepy
import random
from dotenv import load_dotenv
load_dotenv()


def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description[0:140]


def hello_pubsub(event, context):
    fetch_image_and_tweet()


def get(self):
    bucket_name = os.environ.get(os.getenv("BUCKET_NAME"),
                                 app_identity.get_default_gcs_bucket_name())

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
    self.response.write('Using bucket name: ' + bucket_name + '\n\n')


def fetch_image_and_tweet():
    twitter_auth_keys = {
        "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    }
    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)

    bucket_name = os.getenv("BUCKET_NAME")
    storage_client = storage.Client().from_service_account_json(
        os.getenv("SERVICE_JSON_PATH"))
    blobs = storage_client.list_blobs(bucket_name)
    random_blob = random.choice(list(blobs))
    blob_in_bytes = io.BytesIO(random_blob.download_as_string())
    img = Image.open(blob_in_bytes)
    filepath = "/tmp/temp.png"
    img.save(filepath)
    tweet_message = detect_text(filepath)
    api.update_with_media(status=tweet_message, filename=filepath)
