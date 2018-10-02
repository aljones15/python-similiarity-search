import re
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

def eudlidianDistance(df, latitude, longitude):
   return df 

def topTen(df):
    return df.sort_values(by='score', ascending=False).head(10).to_dict('records')
