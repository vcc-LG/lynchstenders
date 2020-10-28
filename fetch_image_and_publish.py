import ipdb
import logging
import os
import cloudstorage as gcs
# import webapp2
from PIL import Image
from pytesseract import image_to_string
from google.cloud import storage
# from google.appengine.api import app_identity
import requests
import tweepy
import random


def get(self):
    bucket_name = os.environ.get('lynchstenders',
                                 app_identity.get_default_gcs_bucket_name())

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Demo GCS Application running from Version: '
                        + os.environ['CURRENT_VERSION_ID'] + '\n')
    self.response.write('Using bucket name: ' + bucket_name + '\n\n')


twitter_auth_keys = {
    "consumer_key": "1paOaozM1IF6s6iMYvIa7NLFH",
    "consumer_secret": "Xj4qnRaaWmGuoXidtgyzCsC7MkqgrIOv838UzfVl5H8qTPBea2",
    "access_token": "1321565465970462720-1YRH2u9iA1xdRJiEVQ7GtG9vn8AJp1",
    "access_token_secret": "LsGKdEeqOT6Oul1FsLrTQNBaNfE26ULlERPcYCG10PoGr"
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

bucket_name = "lynchstenders"

storage_client = storage.Client()

blobs = storage_client.list_blobs(bucket_name)

random_blob = random.choice(list(blobs))

url_lifetime = 3600
serving_url = random_blob.generate_signed_url(url_lifetime)

url_lifetime = 3600
serving_url = random_blob.generate_signed_url(url_lifetime)
request = requests.get(serving_url, stream=True)
filename = 'temp.jpg'
random_blob.download_to_filename(filename)
tweet_message = str(image_to_string(Image.open(filename), lang='eng'))
api.update_with_media(filename, status=tweet_message)
os.remove(filename)