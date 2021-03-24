import json
from flask import Flask, send_from_directory, request, Response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models.Scorer import Scorer


app = Flask(__name__, static_folder='../build')
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


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
    prompt_data_model = PromptDataModel()
    prompt_data = prompt_data_model.return_all()
    prompt_data = prompt_data['prompts']
    response = {datum['json_data'].prompt_id: datum['json_data'].prompt.split('<DIV>') for datum in prompt_data}
    return json.dumps(response)


@app.route('/api/prompt', methods=['POST'])
def get_prompt():
    req_json = request.get_json()
    promptid = req_json['promptid']
    prompt_data_model = PromptDataModel()
    target_prompt = prompt_data_model.find_by_prompt_id(promptid)
    response = target_prompt.prompt.split('<DIV>')
    return json.dumps(response)


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


class PromptDataModel(db.Model):
    __tablename__ = 'prompts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    prompt_uuid = db.Column(db.String(120), unique=True, nullable=False)
    prompt_id = db.Column(db.String, unique=True, nullable=False)
    prompt = db.Column(db.String(120), unique=False, nullable=False)

    def set_data_fields(self, prompt_uuid, prompt_id, prompt):
        self.prompt_uuid = prompt_uuid
        self.prompt_id = str(prompt_id)
        self.prompt = '<DIV>'.join(prompt)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def find_by_prompt_id(cls, prompt_id):
        return cls.query.filter_by(prompt_id=prompt_id).first()

    @classmethod
    def return_all(cls):
        def to_json(json_vals):
            return {
                'json_data': json_vals
            }
        return {'prompts': list(map(lambda x: to_json(x), PromptDataModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
