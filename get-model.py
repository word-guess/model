import zipfile
import urllib.request
import os

urllib.request.urlretrieve(os.getenv("MODEL_URL"), "model.zip")

with zipfile.ZipFile("model.zip", 'r') as zip_ref:
    zip_ref.extractall('./content/')
