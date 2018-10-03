import re
import numpy as np
from similarity.normalized_levenshtein import NormalizedLevenshtein

NORMALIZED_LEVENSHTEIN = NormalizedLevenshtein()

IS_TRUE = re.compile('true', re.IGNORECASE)

def by_name(data_frame, name):
    "produces a normalized distance score between 0 and 1"
    def make_score(_name):
        "make score takes 1 minus the distance to produce the similairty"
        return 1 - NORMALIZED_LEVENSHTEIN.distance(_name, name)
    name_scores = data_frame['name'].map(make_score)
    return name_scores

def by_experience(data_frame, experience):
    "converts the experienced column into a score of 0 or 1"
    params_exper = re.match(IS_TRUE, experience) != None
    def make_score(_exp):
        "returns 1 if the bool from the query string matches the Series experienced value"
        result = params_exper == _exp
        return 1 if result else 0
    exp_score = data_frame['experienced'].map(make_score)
    return exp_score

def by_distance(data_frame, location_type, value):
    "to normalize for all distances 1 - distance / max distance"
    distances = np.square(data_frame[location_type] - value)
    max_distance = np.max(distances)
    normalized = 1 - distances / max_distance
    return normalized

def top_ten(data_frame):
    "pagination query"
    return data_frame.sort_values(by='score', ascending=False).head(10).to_dict('records')
