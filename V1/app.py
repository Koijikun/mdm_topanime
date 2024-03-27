from flask import Flask, jsonify, request, send_file, render_template
import sys
import os

# Get the absolute path of the directory containing the current script (somehow venv cant find it otherwise)
current_dir = os.path.dirname(os.path.abspath(__file__))
scrape_dir = os.path.join(current_dir, 'scrape')
sys.path.append(scrape_dir)

import scrape.data_scrape as ds
import model.model as m


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

@app.route("/predict")
def predict():
    model = m.create_model
    data = request.json
    new_episode = int(data['episode'])
    new_member = int(data['member'])
    new_timespan = int(data['timespan'])

    # Call model_predict function with user input
    prediction = m.model_predict(model, new_episode, new_member, new_timespan)

    return jsonify({'prediction': prediction})
