import random
import json
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn import preprocessing
from utils.feature_utils import get_features_for_one_essay
from utils.readability_utils import get_readability_features_for_one_essay
from utils.basic_utils import get_token_ids, pad_hierarchical_text_sequences
from custom_layers.inner_attention import InnerAttention
from custom_layers.zeromasking import ZeroMaskedEntries
from custom_layers.masked_loss import masked_loss_function


class Scorer():
    def __init__(self, features_path, readability_path, pos_vocabulary_path, model_path):
        self.pos_vocabulary_path = pos_vocabulary_path
        self.features_path = features_path
        self.readability_path = readability_path
        self.model_path = model_path
        self.promptid = None
        self.essay = None
        self.vocab = None
        self.features_df = None
        self.readability_df = None
        self.normalized_essay_features = None
        self.normalized_readability_features = None
        self.padded_tokens = None
        self.model = None
        self.load_vocab()
        self.load_model()
        self.get_existing_linguistic_features()
        self.get_existing_readability_features()

    def load_vocab(self):
        with open(self.pos_vocabulary_path) as f:
            self.vocab = json.load(f)
    
    def load_model(self):
        layers_dict = {'ZeroMaskedEntries': ZeroMaskedEntries, 'InnerAttention': InnerAttention, 'masked_loss_function': masked_loss_function}
        self.model = tf.keras.models.load_model(self.model_path, custom_objects=layers_dict)
    
    def get_existing_linguistic_features(self):
        self.features_df = pd.read_csv(self.features_path)

    def get_existing_readability_features(self):
        self.readability_df = pd.read_csv(self.readability_path)
    
    def get_linguistic_features(self, essay, promptid):
        self.promptid = promptid
        self.essay = essay
        linguistic_features_dict = get_features_for_one_essay(essay)
        prompt_spec_df = self.features_df[self.features_df['prompt_id'] == int(promptid)]
        del prompt_spec_df['item_id']
        del prompt_spec_df['prompt_id']
        del prompt_spec_df['score']
        essay_features = pd.DataFrame(linguistic_features_dict, index=[0])
        min_max_scaler = preprocessing.MinMaxScaler()
        min_max_scaler.fit(prompt_spec_df)
        self.normalized_essay_features = min_max_scaler.transform(essay_features)
    
    def get_readability_features(self):
        readability_features_dict = get_readability_features_for_one_essay(self.essay)
        prompt_spec_df = self.readability_df[self.readability_df['prompt_id'] == int(self.promptid)]
        del prompt_spec_df['essay_id']
        del prompt_spec_df['prompt_id']
        essay_features = pd.DataFrame(readability_features_dict, index=[0])
        min_max_scaler = preprocessing.MinMaxScaler()
        min_max_scaler.fit(prompt_spec_df)
        self.normalized_readability_features = min_max_scaler.transform(essay_features)
    
    def read_essay_data(self):
        essay_tokens = get_token_ids(self.essay, self.vocab)
        padded_tokens = pad_hierarchical_text_sequences(essay_tokens, max_sentnum=70, max_sentlen=50) # hardcoded len/nums
        self.padded_tokens = padded_tokens.reshape((padded_tokens.shape[0], padded_tokens.shape[1] * padded_tokens.shape[2]))

    def get_scores(self):
        print(self.padded_tokens.shape)
        print(self.normalized_essay_features.shape)
        print(self.normalized_readability_features.shape)
        prediction = self.model.predict([self.padded_tokens, self.normalized_essay_features, self.normalized_readability_features])
        print(prediction)
        labels = ["Overall", "Content", "Organization", "Word Choice", "Sentence Fluency", "Conventions"]
        scores = [random.randint(1, 101) for label in labels]
        return {
            'labels': labels,
            'scores': scores
        }