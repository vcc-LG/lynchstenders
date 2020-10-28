import logging
import os
import cloudstorage as gcs
from PIL import Image
from pytesseract import image_to_string
from google.cloud import storage
import requests
import tweepy
import random
from dotenv import load_dotenv
load_dotenv()


def get(self):
    bucket_name = os.environ.get('lynchstenders',
                                 app_identity.get_default_gcs_bucket_name())

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
    self.response.write('Using bucket name: ' + bucket_name + '\n\n')


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

url_lifetime = 3600
serving_url = random_blob.generate_signed_url(url_lifetime)
request = requests.get(serving_url, stream=True)
filename = 'temp.jpg'
random_blob.download_to_filename(filename)
tweet_message = str(image_to_string(Image.open(filename), lang='eng'))
api.update_with_media(filename, status=tweet_message)
os.remove(filename)
