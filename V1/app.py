from flask import Flask, jsonify, request, send_file, render_template
import sys
import os

# Get the absolute path of the directory containing the current script (somehow venv cant find it otherwise)
current_dir = os.path.dirname(os.path.abspath(__file__))
scrape_dir = os.path.join(current_dir, 'scrape')
sys.path.append(scrape_dir)

import scrape.data_scrape as ds
from azure.storage.blob import BlobServiceClient
import pickle
from pathlib import Path

# init app, load model from storage
print("*** Init and load model ***")
if 'AZURE_STORAGE_CONNECTION_STRING' in os.environ:
    azureStorageConnectionString = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(azureStorageConnectionString)

    print("fetching blob containers...")
    containers = blob_service_client.list_containers(include_metadata=True)
    for container in containers:
        existingContainerName = container['name']
        print("checking container " + existingContainerName)
        if existingContainerName.startswith("anime-model"):
            parts = existingContainerName.split("-")
            print(parts)
            suffix = 1
            if (len(parts) == 3):
                newSuffix = int(parts[-1])
                if (newSuffix > suffix):
                    suffix = newSuffix

    container_client = blob_service_client.get_container_client("anime-model-" + str(suffix))
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)

    # Download the blob to a local file
    Path("model").mkdir(parents=True, exist_ok=True)  # Adjusted path
    download_file_path = os.path.join("model", "anime_model.pkl")  # Adjusted path
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())

else:
    print("CANNOT ACCESS AZURE BLOB STORAGE - Please set connection string as env variable")
    print(os.environ)
    print("AZURE_STORAGE_CONNECTION_STRING not set")    

file_path = Path("model", "anime_model.pkl")  # Adjusted path
with open(file_path, 'rb') as fid:
    model = pickle.load(fid)


app = Flask(__name__, static_url_path='/', static_folder='web', template_folder='web')

data = {
    'name': ds.name,
    'episodes': ds.episodes,
    'airing': ds.airing,
    'members': ds.members,
    'ratings': ds.ratings
}

@app.route("/")
def index():
    return render_template('index.html', data=data)

@app.route("/new")
def new():
    return send_file('new.html')

@app.route("/predict", methods=['POST'])
def predict():
    # Get input data from the request
    data = request.get_json()
    
    # Extract input features from the data
    episodes = float(data['episodes'])
    members = float(data['members'])
    timespan = float(data['timespan'])
    
    # Perform prediction using the model
    prediction = model.predict([[episodes, members, timespan]])
    
    # Return the predicted value as JSON response
    return jsonify({'predicted_rating': prediction[0]})  # Assuming prediction is a single value