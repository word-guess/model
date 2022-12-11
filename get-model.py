# import zipfile
import urllib.request
import os

os.mkdir("./content")
urllib.request.urlretrieve(os.getenv("MODEL_URL"), "./content/model.bin")

# with zipfile.ZipFile("model.zip", 'r') as zip_ref:
#     zip_ref.extractall('./content/')
