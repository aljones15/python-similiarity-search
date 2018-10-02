from similarity.normalized_levenshtein import NormalizedLevenshtein
normalized_levenshtein = NormalizedLevenshtein()

def byName(df, name):
    def makeScore(_name):
        return 1 - normalized_levenshtein.distance(_name, name)
    name_scores = df['name'].map(makeScore)
    df['score'] += name_scores

def eudlidianDistance(df, latitude, longitude):
   return df 

def topTen(df):
    return df.sort_values(by='score', ascending=False).head(10).to_dict('records')
