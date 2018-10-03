import numpy as np
import pandas as pd
from numpy.linalg import norm
from similarity.normalized_levenshtein import NormalizedLevenshtein
normalized_levenshtein = NormalizedLevenshtein()

def byName(df, name):
    "produces a normalized distance score between 0 and 1"
    def makeScore(_name):
        return 1 - normalized_levenshtein.distance(_name, name)
    name_scores = df['name'].map(makeScore)
    df['score'] += name_scores

def byExperience(df, experience):
    "converts the experienced column into a score of 0 or 1"
    def makeScore(_exp):
        "pandas bool does not match with django bool"
        result = str(experience) == str(_exp)
        return 1 if result else 0
    exp_score = df['experienced'].map(makeScore) 
    df['score'] += exp_score

def byEudlidianDistance(df, latitude, longitude):
   "to normalize for all distances 1 - distance / max distance"
   searchLocation = pd.Series({'latitude': float(latitude), 'longitude': float(longitude)})
   # distances =np.linalg.norm()
   # np.linalg.norm
   return df 

def bySingleLocation(df, locationType, value):
    distances = np.square(df[locationType] - float(value))
    maxDistance = np.max(distances)
    normalized = 1 - distances / maxDistance
    print(normalized)
    df['score'] += normalized

def topTen(df):
    "pagination query"
    return df.sort_values(by='score', ascending=False).head(10).to_dict('records')
