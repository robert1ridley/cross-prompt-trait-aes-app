from utils.basic_utils import text_tokenizer
import readability


def get_readability_features_for_one_essay(content):
    sent_tokens = text_tokenizer(content, replace_url_flag=True, tokenize_sent_flag=True)
    sentences = [' '.join(sent) + '\n' for sent in sent_tokens]
    sentences = ''.join(sentences)
    readability_scores = readability.getmeasures(sentences, lang='en')
    features = {}
    for cat in readability_scores.keys():
        for subcat in readability_scores[cat].keys():
            ind_score = readability_scores[cat][subcat]
            features[cat + '-' + subcat] = ind_score
    return features
