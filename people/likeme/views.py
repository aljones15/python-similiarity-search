import sys
from django.http import JsonResponse
import pandas as pd
import numpy as np
from pathlib import Path
from .transform import byName, topTen, byExperience, byDistance

def getDataFrame():
    "gets the data frame and sets the score to 0"
    # move to models
    csvPath = Path('./data.csv')
    df = pd.read_csv(csvPath)
    df.loc[:, 'score'] = 0
    return df

# Create your views here.

def index(request):
    try:
        df = getDataFrame()
        params = request.GET
        score_count = 0;

        if 'name' in params:
            name_scores = byName(df, params['name'])
            df['score'] += name_scores
            score_count += 1

        if 'experienced' in params:
            exp_scores = byExperience(df, params['experienced'])
            df['score'] += exp_scores
            score_count += 1

        if 'latitude' in params:
            new_scores = byDistance(df, 'latitude', float(params['latitude']))
            df['score'] += new_scores
            score_count += 1

        if 'longitude' in params:
            new_scores = byDistance(df, 'longitude', float(params['longitude']))
            df['score'] += new_scores
            score_count += 1

        if score_count > 0:
            df['score'] = df['score'] / score_count
            
        results = topTen(df)
        return JsonResponse({'peopleLikeYou': results})

    except KeyError as e:
        response = JsonResponse({'error': 'Unsupported Key'})
        response.status_code = 400;
        return response

    except:
        e = sys.exc_info()[0]
        raise e
        response = JsonResponse({'error': 'Unknown: ' + e.message})
        response.status_code = 400;
        return response

