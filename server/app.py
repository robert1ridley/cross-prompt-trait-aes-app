'''server/app.py - main api app declaration'''
import json
from flask import Flask, send_from_directory, request, Response
from flask_cors import CORS
from models.Scorer import Scorer
from utils.basic_utils import get_prompt_texts_as_dict, get_single_prompt

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
CORS(app)

features_path = 'server/resources/hand_crafted_v3.csv'
readability_path = 'server/resources/allreadability_notnorm.csv'
pos_vocabulary_path = 'server/resources/pos_vocab.json'
model_path = 'server/resources/attribute_attention_v2_sans-prompt-1'
scorer = Scorer(features_path, readability_path, pos_vocabulary_path, model_path)


def validate_request(req_json):
    try:
        original_text = req_json['essayText']
    except (TypeError, KeyError):
        return json.dumps({"error": "Please send the parameter 'text' with your request."}), None
    try:
        prompt_id = req_json['promptID']
    except (TypeError, KeyError):
        return json.dumps({"error": "Please send the parameter 'promptID' with your request."}), None
    if len(original_text) == 0:
        return json.dumps({"error": "Input text too short."}), None
    return None, (original_text, prompt_id)


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
    validation_result, original_params = validate_request(req_json)
    if validation_result:
        return Response(validation_result,
                        status=400, mimetype='application/json')
    original_text, prompt_id = original_params[0], original_params[1]
    scorer.get_linguistic_features(original_text, prompt_id)
    scorer.get_readability_features()
    scorer.read_essay_data()
    all_scores = scorer.get_scores()
    return Response(json.dumps(all_scores), status=200, mimetype='application/json')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return send_from_directory(app.static_folder, 'index.html')
