import re
import numpy as np
import pandas as pd
from numpy.linalg import norm
from similarity.normalized_levenshtein import NormalizedLevenshtein
normalized_levenshtein = NormalizedLevenshtein()

isTrue = re.compile('true', re.IGNORECASE)

def byName(df, name):
    "produces a normalized distance score between 0 and 1"
    def makeScore(_name):
        return 1 - normalized_levenshtein.distance(_name, name)
    name_scores = df['name'].map(makeScore)
    return name_scores

def byExperience(df, experience):
    paramsExper = re.match(isTrue, experience) != None
    "converts the experienced column into a score of 0 or 1"
    def makeScore(_exp):
        result = paramsExper == _exp
        return 1 if result else 0
    exp_score = df['experienced'].map(makeScore)
    return exp_score 

def byDistance(df, locationType, value):
    "to normalize for all distances 1 - distance / max distance"
    distances = np.square(df[locationType] - value)
    maxDistance = np.max(distances)
    normalized = 1 - distances / maxDistance
    return normalized

def topTen(df):
    "pagination query"
    return df.sort_values(by='score', ascending=False).head(10).to_dict('records')
