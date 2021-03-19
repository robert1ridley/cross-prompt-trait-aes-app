'''server/app.py - main api app declaration'''
import json
from flask import Flask, send_from_directory, request
from flask_cors import CORS
from models.Scorer import Scorer
from utils.basic_utils import get_prompt_texts_as_dict, get_single_prompt

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
CORS(app)

scorer = Scorer()


def validate_request(req_json):
    try:
        original_text = req_json['text']
    except (TypeError, KeyError):
        return json.dumps({"error": "Please send the parameter 'text' with your request."}), None
    if len(original_text) == 0:
        return json.dumps({"error": "Input text too short."}), None
    return None, original_text


@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    return json.dumps(get_prompt_texts_as_dict())


@app.route('/api/prompt', methods=['POST'])
def get_prompt():
    req_json = request.get_json()
    promptid = req_json['promptid']
    single_prompt = get_single_prompt(promptid)
    return json.dumps(single_prompt)


@app.route('/api/score', methods=['POST'])
def get_scores():
    req_json = request.get_json()
    all_scores = scorer.get_scores()
    return json.dumps(all_scores)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return send_from_directory(app.static_folder, 'index.html')
